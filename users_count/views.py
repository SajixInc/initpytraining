from django.shortcuts import render
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from django.db.models import Count
from users.models import LoginSignUp
from datetime import datetime, timedelta
import calendar


def user_registration_aggregated(request):
    data = None  # Initialize data
    error = None  # Initialize error messages

    if request.method == 'POST':  # Handle form submission
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        aggregation_level = request.POST.get('level', 'day')  # Default to 'day'

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            if start_date > end_date:
                error = "The 'end date' must be after 'start date'."
            else:
                # Map aggregation levels to Django's Trunc functions
                aggregation_map = {
                    "day": TruncDay,
                    "week": TruncWeek,
                    "month": TruncMonth,
                    "year": TruncYear,
                }

                if aggregation_level not in aggregation_map:
                    error = f"Invalid level '{aggregation_level}'. Valid levels are: day, week, month, year."
                else:
                    trunc_function = aggregation_map[aggregation_level]

                    # Query for aggregated user data
                    user_data = (
                        LoginSignUp.objects.filter(date_created__range=[start_date, end_date])
                        .annotate(period=trunc_function('date_created'))
                        .values('period')
                        .annotate(count=Count('id'))
                        .order_by('period')
                    )

                    # Create full period range and populate missing periods with count = 0
                    period_range = []
                    current_date = start_date

                    while current_date <= end_date:
                        if aggregation_level == "day":
                            period_range.append(current_date.strftime('%Y-%m-%d'))
                            current_date += timedelta(days=1)
                        elif aggregation_level == "week":
                            period_range.append(current_date.strftime('%Y-%m-%d'))
                            current_date += timedelta(weeks=1)
                        elif aggregation_level == "month":
                            period_range.append(current_date.strftime('%Y-%m'))
                            next_month = current_date.month + 1 if current_date.month < 12 else 1
                            next_year = current_date.year + 1 if next_month == 1 else current_date.year
                            current_date = current_date.replace(year=next_year, month=next_month, day=1)
                        elif aggregation_level == "year":
                            period_range.append(current_date.strftime('%Y'))
                            current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)

                    # Map query result to a dictionary
                    user_data_dict = {
                        entry['period'].strftime('%Y-%m-%d' if aggregation_level == 'day' else '%Y-%m'): entry['count']
                        for entry in user_data
                    }

                    # Build the final data list
                    data = [
                        {
                            "period": period,
                            "count": user_data_dict.get(period, 0),
                        }
                        for period in period_range
                    ]
        except (ValueError, TypeError):
            error = "Invalid date format. Please provide dates in 'YYYY-MM-DD' format."

    # Render the HTML template with data and error messages
    return render(request, 'user_count.html', {"data": data, "error": error})
