
from django.core.management.base import BaseCommand

from apps.school.models import ReadingPassage, ReadingQuestion
from apps.school.management.commands.reading_data import A1_READINGS


class Command(BaseCommand):
    help = "Seed LingoRise Reading Bank"

    def handle(self, *args, **options):

        created_passages = 0
        created_questions = 0

        for data in A1_READINGS:

            passage, passage_created = ReadingPassage.objects.get_or_create(
                title=data["title"],
                defaults={
                    "level": data["level"],
                    "topic": data["topic"],
                    "text": data["text"].strip(),
                    "is_active": True,
                },
            )

            if passage_created:
                created_passages += 1

            for item in data["questions"]:

                _, question_created = ReadingQuestion.objects.get_or_create(
                    passage=passage,
                    question=item["question"],
                    defaults={
                        "question_type": "MCQ",
                        "option_a": item["A"],
                        "option_b": item["B"],
                        "option_c": item["C"],
                        "option_d": item["D"],
                        "correct_answer": item["answer"],
                        "explanation": item["explanation"],
                    },
                )

                if question_created:
                    created_questions += 1

        total_passages = ReadingPassage.objects.count()
        total_questions = ReadingQuestion.objects.count()

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "       LingoRise Reading Bank"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"New passages created: {created_passages}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"New questions created: {created_questions}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total passages in database: {total_passages}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total questions in database: {total_questions}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Reading Bank is ready!"
            )
        )

        self.stdout.write("")
