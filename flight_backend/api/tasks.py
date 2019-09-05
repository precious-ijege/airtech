from datetime import datetime, date, timezone

from celery import shared_task
from celery.schedules import crontab
from celery.decorators import periodic_task

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import get_template

from api.models import Ticket
from api.constants import BOOKED, RESERVED


@shared_task()
def flight_booking_notification(pk):
    ticket = get_object_or_404(Ticket.objects.all(), pk=pk)
    if ticket:
        subject = "Details of your booked ticket"
        sender = settings.EMAIL_HOST_USER
        recipient_list = [ticket.user.email]
        details = dict(
            name=ticket.user.first_name,
            ticket_number=ticket.ticket_id,
            flight_number=ticket.flight.flight_number,
            departure=ticket.flight.departure.city,
            destination=ticket.flight.destination.city,
            departure_date=ticket.flight.departure_date,
            passport_number=ticket.passport_number,
            ticket_class=ticket.ticket_class,
        )
        body = get_template("booked.txt").render(details)
        send_mail(subject, body, sender, recipient_list)


@shared_task()
def flight_reservation_notification(pk):
    ticket = get_object_or_404(Ticket.objects.all(), pk=pk)
    if ticket:
        subject = "Details of your reserved ticket"
        sender = settings.EMAIL_HOST_USER
        recipient_list = [ticket.user.email]
        details = dict(
            name=ticket.user.first_name,
            ticket_number=ticket.ticket_id,
            flight_number=ticket.flight.flight_number,
            departure=ticket.flight.departure.city,
            destination=ticket.flight.destination.city,
            departure_date=ticket.flight.departure_date,
            passport_number=ticket.passport_number,
            ticket_class=ticket.ticket_class,
        )
        body = get_template("reserved.txt").render(details)
        send_mail(subject, body, sender, recipient_list)


@periodic_task(
    run_every=(crontab(hour=0, minute=0)),
    name="send_flight_reminder_task",
    ignore_result=True,
)
def send_flight_reminder():
    current_date = date.today()
    tickets = Ticket.objects.filter(status=BOOKED)
    for ticket in tickets:
        if ((ticket.flight.departure_date - current_date).days >= 0) and (
            (ticket.flight.departure_date - current_date).days <= 1
        ):
            subject = "Reminder For Departure of Flight"
            sender = settings.EMAIL_HOST_USER
            recipient_list = [ticket.user.email]
            details = dict(
                name=ticket.user.first_name,
                ticket_number=ticket.ticket_id,
                flight_number=ticket.flight.flight_number,
                departure=ticket.flight.departure.city,
                destination=ticket.flight.destination.city,
                departure_date=ticket.flight.departure_date,
            )
            body = get_template("reminder.txt").render(details)
            send_mail(subject, body, sender, recipient_list)


@periodic_task(
    run_every=(crontab(hour="*/1", minute=0)),
    name="delete_unpaid_reservation",
    ignore_result=True,
)
def delete_unpaid_reserved_tickets():
    current_datetime = datetime.now(timezone.utc)
    tickets = Ticket.objects.filter(status=RESERVED)
    for ticket in tickets:
        if (current_datetime - ticket.created).days >= 1:
            ticket.delete()
