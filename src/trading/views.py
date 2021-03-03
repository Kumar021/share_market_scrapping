import json
import requests
import csv
import pandas as pd 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render 
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Exists, Count, F, Value
from rest_framework import viewsets
from django.conf import settings

from datetime import datetime, date

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from . import serializers 
from rest_framework.permissions import IsAuthenticated 
from rest_framework import permissions, generics, mixins 
from django.template import RequestContext
from django.core import serializers
from django.db.models import Sum
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404


from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

