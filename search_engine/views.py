from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .utils import extract_keywords_from_query, scrape_jobs, parse_resume

class Testing(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print("Hello World")
        return Response({"Message": "Hello world"})


class JobSearchView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        query = request.data.get('query', None)
        location = request.data.get('location', None)
        company = request.data.get('company', None)
        resume_file = request.FILES.get('resume', None)

        if query:
            parsed_query = extract_keywords_from_query(query)
            job_role_search = " ".join(parsed_query['job_roles'] + parsed_query['skills'])
            scraped_jobs = scrape_jobs(job_role_search, location=location, company=company)
            return Response(scraped_jobs)

        if resume_file:
            parsed_resume = parse_resume(resume_file)
            resume_skills_search = " ".join(parsed_resume['skills'])
            scraped_jobs = scrape_jobs(resume_skills_search)
            return Response(scraped_jobs)

        return Response({"error": "No query or resume provided"}, status=400)