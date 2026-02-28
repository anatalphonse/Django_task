class TaskServices:
  @staticmethod
  def complete_task(task, report, hours):
    if not report or not hours:
      raise ValueError("Report and hours required")
    
    task.status = "completed"
    task.completion_report = report
    task.worked_hours = hours
    task.save()
    return task 