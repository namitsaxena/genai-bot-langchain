from langchain.tools import StructuredTool

from src.tools.KubernetesTool import KubernetesTool
from src.tools.PipelineUtility import PipelineUtility
from src.tools.SchedulerUtility import SchedulerUtility
from src.tools.ToolFunctions import get_current_date, get_current_time, some_function, get_bot_name


def get_tools():
    tools = []
    ###################################
    # setup functions
    ###################################
    t_get_current_date = StructuredTool.from_function(
        # Note: func is NOT get_current_date() i.e.
        # the function's reference is sent to the callable rather than executing the function itself.
        func=get_current_date
        # ,name="today's date"
        # ,description="used to lookup today's date",
    )
    tools.append(t_get_current_date)

    tools.append(StructuredTool.from_function(func=get_bot_name))

    tools.append(StructuredTool.from_function(func=get_current_time))

    # gets a random number as described in function docstring
    tools.append(StructuredTool.from_function(func=some_function))

    ###################################
    # setup functions from
    # other classes
    ###################################
    scheduler = SchedulerUtility()
    tools.append(StructuredTool.from_function(scheduler.get_job_status))

    # NOTE: always uses this to answer job status despite all comments if
    # function names are same - whatever comes later gets used in this case
    pipeline = PipelineUtility()
    tools.append(StructuredTool.from_function(pipeline.get_pipeline_job_status, return_direct=True))


    ###################################
    # setup tool classes
    ###################################
    tools.append(KubernetesTool())

    return tools
