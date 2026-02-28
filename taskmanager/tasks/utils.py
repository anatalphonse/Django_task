def can_access_task(user, task):

  if user.role == "superadmin":
    return True
  
  if user.role == "admin":
    return task.assigned_to.admin == user
  
  if user.role == "user":
    return task.assigned_to == user
  
  return False