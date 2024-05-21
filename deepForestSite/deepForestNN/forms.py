from django import forms
from .models import Image_data


class SetImageForm(forms.ModelForm):
    class Meta:
        model = Image_data
        fields = ['source_file']
        widgets = {
            'source_file': forms.ClearableFileInput(attrs={
                'class': 'image_selection',
                'accept': 'image/*'
            })
        }
        labels = {
            'source_file': 'Выберите изображение, на котором хотите обнаружить деревья'
        }

    def clean_source_file(self):
        file = self.cleaned_data.get('source_file')
        if file:
            if not file.content_type.startswith('image/'):
                raise forms.ValidationError('Загруженный файл не является изображением.')
            if file.size > 5 * 1024 * 1024:  # Ограничение размера файла до 5MB
                raise forms.ValidationError('Размер файла не должен превышать 5MB.')
        return file
