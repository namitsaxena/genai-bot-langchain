# Represents kubernetes execution
class KubernetesUtility():

    def __init__(self):
        print("Kubernetes utility initialized..")

    def execute_command(self, namespace, command, kubectl_context="dv-k8-cluster"):
        print(f"Executing command: {command} in (context: {kubectl_context}, namespace: {namespace})")
        return "command_output"

    def delete_pod(self, kubectl_context, namespace, pod_name):
        print(f"Deleting pod: {pod_name} in (context: {kubectl_context}, namespace: {namespace})")
        return True
