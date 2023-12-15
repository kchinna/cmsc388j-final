import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import movie_client, car_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Review
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
    print("CORRECT")
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("movies.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@cars.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = car_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


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


# @movies.route("/user/<username>")
# def user_detail(username):
#     #uncomment to get review image
#     user = User.objects(username=username).first()

#     if user:
#         reviews = Review.objects(commenter=user).order_by("-date")
#         img = get_b64_img(user.username) # use their username for helper function
#         return render_template("user_detail.html",
#                                user=user, 
#                                reviews=reviews,
#                                image=img,
#                                error=None)
#     else:
#         return render_template("user_detail.html", 
#                                user=None, 
#                                reviews=None, 
#                                image=None,
#                                error="User not found.")
