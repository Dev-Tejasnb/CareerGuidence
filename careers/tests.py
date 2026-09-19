from django.test import TestCase

from careers.models import Career, CareerSkill
from careers.services import analyze_career
from skills.models import Skill


class AnalyzeCareerTests(TestCase):
    def setUp(self):
        self.python = Skill.objects.create(name="Python")
        self.sql = Skill.objects.create(name="SQL")
        self.comms = Skill.objects.create(name="Communication", category="soft")
        self.career = Career.objects.create(title="Data Scientist")
        CareerSkill.objects.create(career=self.career, skill=self.python, importance=5)
        CareerSkill.objects.create(career=self.career, skill=self.sql, importance=3)
        CareerSkill.objects.create(career=self.career, skill=self.comms, importance=4)

    def test_full_proficiency_scores_100(self):
        ratings = {self.python.id: 5, self.sql.id: 4, self.comms.id: 4}
        result = analyze_career(self.career, ratings)
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["gaps"], [])
        self.assertEqual(len(result["strengths"]), 3)

    def test_gaps_are_identified_and_weighted(self):
        ratings = {self.python.id: 2, self.sql.id: 5, self.comms.id: 3}
        result = analyze_career(self.career, ratings)
        # weight: python(5) ratio 2/4, sql(3) ratio 1, comms(4) ratio 3/4
        expected = round(((0.5 * 5 + 1.0 * 3 + 0.75 * 4) / 12) * 100)
        self.assertEqual(result["score"], expected)
        self.assertEqual(len(result["gaps"]), 2)
        # most important gap (Python, importance 5) sorts first
        self.assertEqual(result["gaps"][0]["skill"], self.python)

    def test_unrated_skill_counts_as_gap(self):
        result = analyze_career(self.career, {})
        self.assertEqual(len(result["gaps"]), 3)
        self.assertEqual(result["score"], 0)