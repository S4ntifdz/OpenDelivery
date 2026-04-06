from django.db import models

from core.models import BaseModel
from routing.enums import TaskType


class TaskModel(BaseModel):
    stop = models.ForeignKey(
        "routing.StopModel",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")

    class Meta:
        db_table = "routing_task"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"Task {self.type} @ Stop {self.stop_id}"
