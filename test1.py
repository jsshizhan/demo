from prefect import flow,task
from prefect_dask.task_runners import DaskTaskRunner
from prefect.deployments import run_deployment,Deployment


@task
def hello_dask():
    print("Hello from Dask1!")

@flow#(task_runner=DaskTaskRunner(address="tcp://localhost:8786"))
def subflow():
    hello_dask.submit()


@flow(log_prints=True)
def buy():
    run_deployment(
        name="deployment_subflow",
    )
    print("Buying securities1")


if __name__ == "__main__":
    buy.from_source(
        source="https://github.com/jsshizhan/demo.git", 
        entrypoint="test1.py:subflow"
    ).deploy(name="deployment_subflow",work_pool_name="desktop-pool")

    buy.from_source(
        source="https://github.com/jsshizhan/demo.git", 
        entrypoint="test1.py:buy"
    ).deploy(name="deployment",work_pool_name="process_pool")
