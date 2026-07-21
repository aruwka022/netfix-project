from django import template

register = template.Library()

FIELD_ICONS = {
    'Air Conditioner': '❄️',
    'All in One': '🛠️',
    'Carpentry': '🪚',
    'Electricity': '⚡',
    'Gardening': '🌿',
    'Home Machines': '🧺',
    'Housekeeping': '🧹',
    'Interior Design': '🛋️',
    'Locks': '🔐',
    'Painting': '🎨',
    'Plumbing': '🚿',
    'Water Heaters': '🔥',
}


@register.filter
def field_icon(field):
    return FIELD_ICONS.get(field, '✨')


@register.filter
def field_slug(field):
    return field.lower().replace(' ', '-')


@register.filter
def stars(rating):
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        rating = 0
    rating = max(0, min(5, rating))
    return '★' * rating + '☆' * (5 - rating)
