from typing import Iterable, List, Tuple

from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags

from .models import Season, Divisions, Singles, ScoreKeepers


def send_mass_html_mail(data_tuples: List[Tuple[str, str, str, str, str]], fail_silently=False, user=None, password=None,
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in data_tuples:
        message = EmailMultiAlternatives(subject, text, from_email, [recipient])
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


def send_roster_emails(year: int, seasons: Iterable[Season]):
    data_tuples = [personalize_roster(year, s) for s in seasons]
    send_mass_html_mail(data_tuples)


def personalize_roster(year: int, season: Season) -> Tuple[str, str, str, str, str]:
    context = {'season': season, 'year': year}
    html_content = render_to_string('roster_email.html', context)
    text_content = strip_tags(html_content)
    return "2021 WWTL Season", text_content, html_content, "league@williamsportwomenstennisleague.com", season.player.user.email

def send_match_cards(all_singles: List[Singles], score_keeper: ScoreKeepers):
    data_tuples = [generate_email(singles, score_keeper) for singles in all_singles if singles.player.player.user.email]
    send_mass_html_mail(data_tuples)


def generate_email(singles: Singles, score_keeper: ScoreKeepers) -> Tuple[str, str, str, str, str]:
    home_matches = singles.home_matches.all()
    away_matches = singles.away_matches.all()
    opponents = [m.away for m in home_matches] + [m.home for m in away_matches]
    context = {"opponents": opponents, "singles": singles, "score_keeper": score_keeper}
    html_content = render_to_string('singles_match_card.html', context)
    text_content = strip_tags(html_content)
    return "2021 WWTL Match Card", text_content, html_content, "league@williamsportwomenstennisleague.com", singles.player.player.user.email
