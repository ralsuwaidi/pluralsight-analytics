from dataclasses import dataclass
from typing import Optional


@dataclass
class Skill:
    quintileLevel: str
    measurementType: str
    skillName: str

    @property
    def is_expert(self):
        return "expert" in self.quintileLevel

    @property
    def is_above_average(self):
        return "above-average" in self.quintileLevel

    def __repr__(self):
        return self.skillName


@dataclass
class User:
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    nationality: Optional[str]
    country_residence: Optional[str]
    academic_qualification: Optional[str]
    mobile_number: Optional[str]
    is_seeking_job: bool
    is_working: bool
    employer: Optional[str]
    years_experience: Optional[int]
    employment_time: Optional[str]
    github: Optional[str]
    linkedin: Optional[str]
    personal_site: Optional[str]
    fav_language: Optional[str]
    about: Optional[str]
    proud_project: Optional[str]
    created_at: Optional[str]
    user: Optional[str]
    updated_at: Optional[str]
    skills: list

    @property
    def is_local(self):
        return self.nationality == "AE"

    @property
    def is_expert(self):
        for skill in self.skills:
            if skill.is_expert:
                return True
        return False

    @property
    def is_above_average(self):
        for skill in self.skills:
            if skill.is_above_average:
                return True
        return False

    def __repr__(self):
        return "user:" + self.first_name + " " + self.last_name
