FROM python:3.10.1-alpine
RUN pip install boto3
ADD switch-role.py /switch-role.py
ENTRYPOINT ["python", "/switch-role.py"]
