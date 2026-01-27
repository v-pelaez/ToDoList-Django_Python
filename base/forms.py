from django import forms
from django.utils import timezone

from .models import Task


class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = [
        ('1', 'Baja'),
        ('2', 'Media'),
        ('3', 'Alta'),
    ]

    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        label="Prioridad",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'deadline', 'priority', 'tags_raw']

        # Traducción de nombres de campos
        labels = {
            'title': 'Título de la tarea',
            'description': 'Descripción',
            'completed': '¿Completada?',
            'deadline': 'Fecha límite',
            'tags_raw': 'Etiquetas (separadas por coma)',
        }

        #  Selector de fecha
        widgets = {
            'deadline': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags_raw': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej. casa, urgente, trabajo'}),
        }

    # Título (longitud mínima)
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) < 3:
            raise forms.ValidationError("El título es demasiado corto (mínimo 3 caracteres).")
        return title

    # Etiquetas (evitar caracteres extraños)
    def clean_tags_raw(self):
        tags = self.cleaned_data.get('tags_raw')
        if tags:

            if any(char in tags for char in "#@$"):
                raise forms.ValidationError("Las etiquetas no deben contener símbolos (#, @, $).")
        return tags

    # Fecha límite (no permitir fechas pasadas)
    def clean(self):
        cleaned_data = super().clean()
        deadline = cleaned_data.get('deadline')
        completed = cleaned_data.get('completed')

        # No permitir crear tareas con fecha pasada a no ser que ya estén completadas
        if deadline and deadline < timezone.now().date() and not completed:
            self.add_error('deadline', "La fecha límite no puede ser anterior a hoy.")

        return cleaned_data


class TaskCreateForm(TaskForm):  # Heredamos del anterior y modificamos
    class Meta(TaskForm.Meta):
        # Excluimos el campo 'completed'
        exclude = ['completed']
