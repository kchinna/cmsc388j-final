import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import movie_client, car_client
from ..forms import CarReviewForm, SearchForm, CarRatingForm
from ..models import User, Review, Rating
from ..utils import current_time

cars = Blueprint("cars", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """


@cars.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("cars.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@cars.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        # results = movie_client.search(query)
        results = car_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


@cars.route("/cars/<make>/<model_id>", methods=["GET", "POST"])
def car_detail(make, model_id):
    try:
        models = car_client.search(make)
        result = None
        for m in models:
            print(type(m["Model_ID"]))
            if m["Model_ID"] == int(model_id):
                result = m
                break
        if result == None:
            return render_template("car_detail.html", error_msg="Could not find model for make")
    except ValueError as e:
        return render_template("car_detail.html", error_msg=str(e))
    
    form = CarReviewForm()
    if form.validate_on_submit():
        img = get_b64_img(current_user.username)
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=model_id,
            movie_title=make,
            image=img
        )
        review.save()
        return redirect(request.path)

    rate_form = CarRatingForm()
    if rate_form.validate_on_submit():
        ratings = Rating.objects(rater=current_user._get_current_object(), model_id=model_id, make=make)
        # Can only rate once, won't count otherwise
        if len(ratings) == 0:
            rating = Rating(
                rater=current_user._get_current_object(),
                rating=rate_form.rating.data,
                model_id=model_id,
                make=make
            )
            rating.save()
        return redirect(request.path)
    
    ratings = Rating.objects(model_id=model_id, make=make)
    total = 0
    length = 0
    for r in ratings:
        total += r.rating
        length += 1
    car_rating = 0 if length == 0 else total / length
    print(car_rating)
    
    reviews = Review.objects(imdb_id=model_id)
    return render_template("car_detail.html", form=form, rate_form=rate_form, car=result, reviews=reviews, ratings=ratings, rating=car_rating)


# @movies.route("/movies/<movie_id>", methods=["GET", "POST"])
# def movie_detail(movie_id):
#     try:
#         result = movie_client.retrieve_movie_by_id(movie_id)
#     except ValueError as e:
#         return render_template("movie_detail.html", error_msg=str(e))

#     form = MovieReviewForm()
#     if form.validate_on_submit():
#         img = get_b64_img(current_user.username)

#         review = Review(
#             commenter=current_user._get_current_object(),
#             content=form.text.data,
#             date=current_time(),
#             imdb_id=movie_id,
#             movie_title=result.title,
#             image=img
#         )

#         review.save()

#         return redirect(request.path)

#     reviews = Review.objects(imdb_id=movie_id)

#     return render_template(
#         "movie_detail.html", form=form, movie=result, reviews=reviews
#     )


@cars.route("/user/<username>")
def user_detail(username):
    #uncomment to get review image
    user = User.objects(username=username).first()

    if user:
        reviews = Review.objects(commenter=user).order_by("-date")
        img = get_b64_img(user.username) # use their username for helper function
        return render_template("user_detail.html",
                               user=user, 
                               reviews=reviews,
                               image=img,
                               error=None)
    else:
        return render_template("user_detail.html", 
                               user=None, 
                               reviews=None, 
                               image=None,
                               error="User not found.")
