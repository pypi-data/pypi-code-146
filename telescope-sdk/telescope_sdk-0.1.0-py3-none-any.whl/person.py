from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from telescope_sdk.common import IngestedDataType, Location, Source
from telescope_sdk.utils import (
    convert_country_name_to_iso_code,
    convert_date_string_to_datetime_string,
    get_current_datetime_aws_format,
)


class CanonicalJobTitle(BaseModel):
    title: str
    confidence: Decimal


class ExperienceCompany(BaseModel):
    name: Optional[str] = None
    linkedin_internal_id: Optional[str] = None
    linkedin_url: Optional[str] = None
    location: Optional[Location] = None
    website: Optional[str] = None

    @staticmethod
    def from_pdl(pdl_input: dict[str, any]) -> Optional['ExperienceCompany']:
        location = pdl_input.get('location')
        return ExperienceCompany(
            name=pdl_input.get('name'),
            linkedin_internal_id=pdl_input.get('linkedin_id'),
            linkedin_url=pdl_input.get('linkedin_url'),
            website=pdl_input.get('website'),
            location=Location.from_pdl(location) if location else None
        )


class Experience(BaseModel):
    company: Optional[ExperienceCompany] = None
    start_datetime: Optional[str] = None
    end_datetime: Optional[str] = None
    is_primary: Optional[bool] = None
    job_title: Optional[str] = None
    job_title_levels: Optional[list[str]] = None

    @staticmethod
    def from_pdl(pdl_input: dict[str, any]) -> Optional['Experience']:
        title = pdl_input.get('title', {}) or {}
        company = pdl_input.get('company')
        start_date = pdl_input.get('start_date')
        end_date = pdl_input.get('end_date')
        return Experience(
            company=ExperienceCompany.from_pdl(company) if company else None,
            start_datetime=convert_date_string_to_datetime_string(start_date) if start_date else None,
            end_datetime=convert_date_string_to_datetime_string(end_date) if end_date else None,
            is_primary=pdl_input.get('is_primary'),
            job_title=title.get('name'),
            job_title_levels=title.get('levels')
        )


class Degree(BaseModel):
    levels: Optional[list[str]] = None
    majors: Optional[list[str]] = None


class Education(BaseModel):
    degree: Optional[Degree] = None
    institution_logo_url: Optional[str] = None
    institution_name: Optional[str] = None
    institution_linkedin_url: Optional[str] = None
    start_datetime: Optional[str] = None
    end_datetime: Optional[str] = None

    @staticmethod
    def from_pdl(pdl_input: dict[str, any]) -> Optional['Education']:
        school = pdl_input.get('school', {}) or {}
        start_date = pdl_input.get('start_date')
        end_date = pdl_input.get('end_date')
        return Education(
            degree=Degree(
                levels=pdl_input.get('degrees'),
                majors=pdl_input.get('majors')
            ),
            institution_logo_url=None,
            institution_name=school.get('name'),
            institution_linkedin_url=school.get('linkedin_url'),
            start_datetime=convert_date_string_to_datetime_string(start_date) if start_date else None,
            end_datetime=convert_date_string_to_datetime_string(end_date) if end_date else None
        )


class Language(BaseModel):
    name: Optional[str] = None
    proficiency: Optional[int] = None


class Person(IngestedDataType):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    pdl_id: Optional[str] = None
    headline: Optional[str] = None
    about: Optional[str] = None
    email: Optional[str] = None
    personal_emails: Optional[list[str]] = None
    phone_numbers: Optional[list[str]] = None
    linkedin_url: Optional[str] = None
    linkedin_internal_id: Optional[str] = None
    industry: Optional[str] = None
    company_id: Optional[str] = None
    job_title: Optional[str] = None
    canonical_job_titles: Optional[list[CanonicalJobTitle]] = None
    job_title_levels: Optional[list[str]] = None
    job_role_description: Optional[str] = None
    job_start_date: Optional[str] = None
    company_name: Optional[str] = None
    company_linkedin_url: Optional[str] = None
    company_industry: Optional[str] = None
    company_year_founded: Optional[int] = None
    job_last_updated: Optional[str] = None
    interests: Optional[list[str]] = None
    skills: Optional[list[str]] = None
    experience: Optional[list[Experience]] = None
    education: Optional[list[Education]] = None
    languages: Optional[list[Language]] = None
    location: Optional[Location] = None
    tags: Optional[list[str]] = None
    uploaded_by_user_id: Optional[str] = None
    last_enriched_at: Optional[str] = None

    @staticmethod
    def from_pdl(pdl_input: dict[str, any]) -> Optional['Person']:
        first_name = pdl_input.get('first_name')
        last_name = pdl_input.get('last_name')
        pdl_id = pdl_input.get('id')
        if not first_name or not last_name or not pdl_id:
            return None

        country = pdl_input.get('location_country')
        job_start_date = pdl_input.get('job_start_date')
        job_last_updated = pdl_input.get('job_last_updated')

        return Person(
            id=pdl_id,
            source=Source.PDL,
            version=0,
            created_at=get_current_datetime_aws_format(),
            updated_at=get_current_datetime_aws_format(),
            first_name=first_name,
            last_name=last_name,
            middle_name=pdl_input.get('middle_name'),
            pdl_id=pdl_id,
            headline=None,
            about=pdl_input.get('summary'),
            email=pdl_input.get('work_email'),
            personal_emails=pdl_input.get('personal_emails'),
            phone_numbers=pdl_input.get('phone_numbers'),
            linkedin_url=pdl_input.get('linkedin_url'),
            linkedin_internal_id=pdl_input.get('linkedin_id'),
            industry=pdl_input.get('industry'),
            company_id=pdl_input.get('job_company_linkedin_id'),
            job_title=pdl_input.get('job_title'),
            canonical_job_titles=None,
            job_title_levels=pdl_input.get('job_title_levels'),
            job_role_description=pdl_input.get('job_summary'),
            job_start_date=convert_date_string_to_datetime_string(job_start_date) if job_start_date else None,
            company_name=pdl_input.get('job_company_name'),
            company_linkedin_url=pdl_input.get('job_company_linkedin_url'),
            company_industry=pdl_input.get('job_company_industry'),
            company_year_founded=pdl_input.get('job_company_founded'),
            job_last_updated=convert_date_string_to_datetime_string(job_last_updated) if job_last_updated else None,
            interests=pdl_input.get('interests'),
            skills=pdl_input.get('skills'),
            experience=[Experience.from_pdl(experience) for experience in pdl_input.get('experience', [])],
            education=[Education.from_pdl(education) for education in pdl_input.get('education', [])],
            languages=[Language.parse_obj(language) for language in pdl_input.get('languages', [])],
            location=Location(
                line_1=pdl_input.get('location_street_address'),
                line_2=pdl_input.get('location_address_line_2'),
                country=convert_country_name_to_iso_code(country) if country else None,
                state=pdl_input.get('location_region'),
                postal_code=pdl_input.get('location_postal_code'),
                city=pdl_input.get('location_locality')
            ),
            tags=pdl_input.get('tags'),
            uploaded_by_user_id=None,
            last_enriched_at=get_current_datetime_aws_format()
        )
