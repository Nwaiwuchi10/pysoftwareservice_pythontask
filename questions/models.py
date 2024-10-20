from django.db import models

# Create your models here.
from ckeditor.fields import RichTextField
from fakeModels import SubjectCategoryMapping, Subjects, Answers  # Assumed imported models

def questions_image_storage_path(instance, filename):
    # Define the storage path for images
    return f'questions/{filename}'

class Question(models.Model):
    SEVERITY = [("1", "Basic"), ("2", "Medium"), ("3", "High"), ("4", "Advanced"), ("5", "Highest")]
    category = models.ForeignKey(SubjectCategoryMapping, on_delete=models.CASCADE)
    multiple_quiz_use_subject = models.ManyToManyField(Subjects, related_name="quiz_questions")
    question_severity = models.CharField(null=True, blank=True, max_length=1, choices=SEVERITY)
    question_preamble = RichTextField(help_text="Any preamble or Information needed for the main question", default="", null=True, blank=True)
    question_main = RichTextField(help_text="Question", null=True, blank=True, max_length=50000)
    question_main_image = models.ImageField(upload_to=questions_image_storage_path, null=True, blank=True, help_text="Upload image in place of Text main question")
    question_remark_for_reviewer = models.TextField(null=True, blank=True)
    question_image_preamble = models.ImageField(upload_to=questions_image_storage_path, null=True, blank=True)
    question_set_by = models.CharField(max_length=200, null=False, blank=False)
    question_authorised_by = models.CharField(max_length=200, null=True, blank=True)
    question_ready_for_review = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    authorised_date = models.DateTimeField(null=True, blank=True)
    year_of_past_question = models.DateField(null=True, blank=True)
    question_label = models.CharField(max_length=1000, blank=True, null=True)
    a = models.TextField(null=True, blank=True)
    a_image = models.ImageField(upload_to=questions_image_storage_path, null=True, blank=True)
    b = models.TextField(null=False, blank=False)
    b_image = models.ImageField(upload_to=questions_image_storage_path, null=True, blank=True)
    c = models.TextField(null=False, blank=False)
    c_image = models.ImageField(upload_to=questions_image_storage_path, null=True, blank=True)
    d = models.TextField(null=False, blank=False)
    d_image = models.ImageField(upload_to=questions_image_storage_path, null=True, blank=True)
    e = models.TextField(null=True, blank=True)
    e_image = models.ImageField(upload_to=questions_image_storage_path, null=True, blank=True)
    hidden = models.BooleanField(default=False, null=False, blank=False)
    explanation = models.TextField(null=True, blank=True)
    answer = models.ManyToManyField(Answers)
    assessment_weight = models.PositiveSmallIntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_main[:50]
