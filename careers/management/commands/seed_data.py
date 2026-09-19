from django.core.management.base import BaseCommand

from careers.models import Career, CareerSkill
from skills.models import Skill


SKILLS = {
    # Technical
    "Python": ("technical", "General-purpose programming language used in web, data, and automation."),
    "JavaScript": ("technical", "Language for interactive web pages and modern frontend development."),
    "SQL": ("technical", "Query language for working with relational databases."),
    "Data Analysis": ("technical", "Inspecting, cleaning, and modeling data to find insights."),
    "Machine Learning": ("technical", "Building models that learn from data to make predictions."),
    "Web Frameworks": ("technical", "Using frameworks like Django or React to build applications."),
    "Cloud Computing": ("technical", "Delivering services over the internet via providers like AWS/Azure."),
    "Networking": ("technical", "Designing and managing computer networks and infrastructure."),
    "Cybersecurity": ("technical", "Protecting systems, networks, and data from threats."),
    "UI/UX Design": ("technical", "Designing user interfaces and usable experiences."),
    # Soft
    "Communication": ("soft", "Clearly conveying ideas in writing and speaking."),
    "Problem Solving": ("soft", "Approaching challenges logically to find effective solutions."),
    "Teamwork": ("soft", "Collaborating effectively with others toward shared goals."),
    "Leadership": ("soft", "Guiding and motivating teams to achieve objectives."),
    "Time Management": ("soft", "Organizing time to be productive and meet deadlines."),
    "Adaptability": ("soft", "Adjusting quickly to change and new information."),
}

CAREERS = {
    "Software Developer": {
        "description": "Designs, builds, and maintains software applications.",
        "salary_range": "$75k - $130k",
        "demand_level": "High",
        "skills": {"Python": 5, "JavaScript": 4, "SQL": 3, "Web Frameworks": 4,
                   "Problem Solving": 4, "Teamwork": 3, "Time Management": 3},
    },
    "Data Scientist": {
        "description": "Analyzes complex data to guide business decisions.",
        "salary_range": "$90k - $150k",
        "demand_level": "Very High",
        "skills": {"Python": 5, "SQL": 4, "Data Analysis": 5, "Machine Learning": 5,
                   "Statistics": 0, "Problem Solving": 4, "Communication": 4},
    },
    "Cybersecurity Analyst": {
        "description": "Protects an organization's systems and data from threats.",
        "salary_range": "$80k - $130k",
        "demand_level": "High",
        "skills": {"Networking": 4, "Cybersecurity": 5, "Python": 3, "Cloud Computing": 3,
                   "Problem Solving": 4, "Adaptability": 4},
    },
    "Cloud Engineer": {
        "description": "Designs and manages cloud-based infrastructure and services.",
        "salary_range": "$95k - $145k",
        "demand_level": "Very High",
        "skills": {"Cloud Computing": 5, "Networking": 4, "Python": 4, "Linux": 0,
                   "Problem Solving": 4, "Communication": 3},
    },
    "Product Designer": {
        "description": "Creates user-friendly interfaces and experiences for products.",
        "salary_range": "$70k - $120k",
        "demand_level": "Medium",
        "skills": {"UI/UX Design": 5, "JavaScript": 3, "Communication": 5,
                   "Teamwork": 4, "Adaptability": 4, "Problem Solving": 4},
    },
}

# Skills referenced but not in SKILLS dict (kept out of self-assessment on purpose)
EXTRA_SKILLS = {
    "Statistics": ("technical", "Mathematical methods to collect and analyze data."),
    "Linux": ("technical", "Open-source operating system used widely in servers."),
}


class Command(BaseCommand):
    help = "Seed the database with sample skills and careers."

    def handle(self, *args, **options):
        all_skills = {**SKILLS, **EXTRA_SKILLS}
        for name, (category, description) in all_skills.items():
            Skill.objects.get_or_create(
                name=name,
                defaults={"category": category, "description": description},
            )

        skill_objs = {s.name: s for s in Skill.objects.all()}

        for title, data in CAREERS.items():
            career, _ = Career.objects.get_or_create(
                title=title,
                defaults={
                    "description": data["description"],
                    "salary_range": data["salary_range"],
                    "demand_level": data["demand_level"],
                },
            )
            for skill_name, importance in data["skills"].items():
                if importance == 0:
                    continue
                skill = skill_objs.get(skill_name)
                if not skill:
                    self.stdout.write(self.style.WARNING(f"Missing skill: {skill_name}"))
                    continue
                CareerSkill.objects.get_or_create(
                    career=career,
                    skill=skill,
                    defaults={"importance": importance},
                )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(all_skills)} skills and {len(CAREERS)} careers."
        ))