FROM python:3.9.2-alpine
RUN pip install boto3
ADD switch-role.py /switch-role.py
ENTRYPOINT ["python", "/switch-role.py"]
