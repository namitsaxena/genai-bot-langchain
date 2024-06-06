# Represents kubernetes execution
from typing import Type, Optional

from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from src.utils.KubernetesUtility import KubernetesUtility


class KubernetesCommandInput(BaseModel):
    command: str = Field(description="should be a kubernetes command")
    namespace: str = Field(description="should be a kubernetes namespace")


class KubernetesExecutor(BaseTool):
    name = "kubernetes_helper"
    description = "useful for when you need to interact with kubernetes or gke clusters"
    args_schema: Type[BaseModel] = KubernetesCommandInput

    def __init__(self):
        print("Kubernetes simulator executor initialized..")
        # NOTE:
        # * any self.variable would give error
        # * if super not called then
        # AttributeError: 'KubernetesExecutor' object has no attribute 'args_schema'
        super().__init__()

    def _run(
            self, command: str, namespace: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        # if self.kubernetes_util is None:
        return self.execute_command(command, namespace)

    async def _arun(
            self, command: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("execute_command does not support async")

    def execute_command(self, namespace, command, kubectl_context="aaa"):
        print(f"Executing command: {command} in (context: {kubectl_context}, namespace: {namespace})")
        return """
        NAME                                READY   STATUS    RESTARTS   AGE
        pod-1                               1/1     Running   0          1m
        pod-2                               1/1     Running   0          1m        
        """

    def delete_pod(self, kubectl_context, namespace, pod_name):
        print(f"Deleting pod: {pod_name} in (context: {kubectl_context}, namespace: {namespace})")
        return True
