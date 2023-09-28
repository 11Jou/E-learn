from django import forms

class CourseForm(forms.Form):
    courseName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Course Name'}) , required=True, label="Name")
    courseImage = forms.ImageField(required=True , label="Image")
    Desc = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'placeholder': 'Description', 'rows':4}) , required=True , label="Description")
    courseType = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Course Type'}) , required=True, label="Type")


class LessonForm(forms.Form):
    lessonName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Lesson Name'}) , required=True, label="Name")
    content = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Content'}) , required=True , label="Content")



class SectionForm(forms.Form):
    sectionName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Section Name'}) , required=True, label="Name")
    content = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Content'}) , required=True , label="Content")
    pdf = forms.FileField(required=True , label='Section PDF')
    video = forms.FileField(required=True , label='Section Video')

class OnlineSectionForm(forms.Form):
    sectionName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Section Name'}) , required=True, label="Name")
    content = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Content'}) , required=True , label="Content")
    pdf = forms.FileField(required=True , label='Section PDF')
    start_time = forms.DateTimeField(required=True, label="Section Date", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    url = forms.URLField(required=True, label="Meeting Link")
