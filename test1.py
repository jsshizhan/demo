from prefect import flow,task
from prefect.deployments import run_deployment,Deployment


@task
def hello_dask():
    print("Hello from task!")

@flow(flow_run_name="subflow")
def subflow():
    print("subflow")
    return hello_dask.submit()


@flow(log_prints=True,flow_run_name="root_flow")
def buy():
    run_deployment(
        name="subflow/deployment_subflow",
    )
    print("root flow")


if __name__ == "__main__":
    buy.from_source(
        source="https://github.com/jsshizhan/demo.git", 
        entrypoint="test1.py:subflow"
    ).deploy(name="deployment_subflow",work_pool_name="desktop-pool")

    buy.from_source(
        source="https://github.com/jsshizhan/demo.git", 
        entrypoint="test1.py:buy"
    ).deploy(name="deployment",work_pool_name="process_pool")
