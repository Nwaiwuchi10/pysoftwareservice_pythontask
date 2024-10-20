import re
import os
from PyPDF2 import PdfReader
from django.core.management.base import BaseCommand
from questions.models import Question

class Command(BaseCommand):
    help = "Populate the QUESTION_TABLE from a PDF file"

    def handle(self, *args, **kwargs):
        # Path to the PDF file
        pdf_path = 'path/to/Principles_of_Accounts_1994.pdf'
        if not os.path.exists(pdf_path):
            self.stdout.write(self.style.ERROR(f'{pdf_path} does not exist.'))
            return

        # Read the PDF
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        # Regular expression to capture questions and options
        question_pattern = re.compile(
            r"(\d+)\.(.*?)\nA\.(.*?)\nB\.(.*?)\nC\.(.*?)\nD\.(.*?)\n",
            re.DOTALL
        )

        # Iterate over the matches and create Question instances
        for match in question_pattern.finditer(text):
            question_number, question_main, a, b, c, d = match.groups()

            # Create the Question object
            question = Question(
                question_main=question_main.strip(),
                a=a.strip(),
                b=b.strip(),
                c=c.strip(),
                d=d.strip(),
                question_set_by="Unknown",
                question_ready_for_review=True
            )
            question.save()
            self.stdout.write(self.style.SUCCESS(f'Saved question {question_number}'))
