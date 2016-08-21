""" api.py - the main questions API """

# Import utils
from utils import logger
from utils import generate_password, get_author
# from utils import get_by_urlsafe, get_player, get_limit_offset

import endpoints
from protorpc import remote, messages

from models import BlogEntry, Author

#from models import Game, Player, Question, Match, History
#from models import StringMessage, AnswerMessage
#from models import ScoreForms, ScoreForm, MatchForm, MatchForms
#from models import GameForm, GameForms, ProfileForm, QuestionForm


# ==================== ResourceContainer definitions ====================
# ==================== Resource creation requests    ====================
# NEW_PLAYER_REQUEST = endpoints.ResourceContainer(
#         user_name=messages.StringField(1, required=True),
#         email_address=messages.StringField(2, required=True))

# NEW_GAME_REQUEST = endpoints.ResourceContainer(
#         user_name=messages.StringField(1, required=True),
#         title=messages.StringField(2, required=True))

# NEW_MATCH_REQUEST = endpoints.ResourceContainer(
#         urlsafe_game_key=messages.StringField(1, required=True),
#         user_name=messages.StringField(2, required=True),
#         start_game=messages.BooleanField(3))

# NEW_QUESTION_REQUEST = endpoints.ResourceContainer(
#         question=messages.StringField(1, required=True),
#         correct_answer=messages.StringField(2, required=True),
#         incorrect_answers=messages.StringField(3, repeated=True),
#         urlsafe_game_key=messages.StringField(4, required=True))


# # ==================== Resource retrieval requests   ====================
# ANSWER_REQUEST = endpoints.ResourceContainer(
#         user_name=messages.StringField(1, required=True),
#         urlsafe_question_key=messages.StringField(2, required=True),
#         answer=messages.StringField(3, required=True),
#         urlsafe_match_key=messages.StringField(4, required=True),
#         round=messages.IntegerField(5, required=True))

# QUESTION_GAME_REQUEST = endpoints.ResourceContainer(
#         urlsafe_game_key=messages.StringField(1, required=True),
#         urlsafe_question_key=messages.StringField(2, required=True))

# PROFILE_REQUEST = endpoints.ResourceContainer(
#         user_name=messages.StringField(1, required=True))

# GET_ENTITY_REQUEST = endpoints.ResourceContainer(
#         urlsafe_key=messages.StringField(1, required=True),
#         user_name=messages.StringField(2, required=True),
#         start_game=messages.BooleanField(3))

# GET_QUESTION_REQUEST = endpoints.ResourceContainer(
#         urlsafe_match_key=messages.StringField(1, required=True))

# LIST_REQUEST = endpoints.ResourceContainer(
#         page=messages.IntegerField(1, required=True),
#         user_name=messages.StringField(2))

# ================ Various ================
class StringMessage(messages.Message):
    """ Outbound string message (string) """
    message = messages.StringField(1, required=True)

# NEW_AUTHOR_REQUEST
NEW_AUTHOR_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1, required=True),
    email_address=messages.StringField(2, required=True),
    password=messages.StringField(3, required=True))

NEW_BLOG_ENTRY_REQUEST = endpoints.ResourceContainer(
    title=messages.StringField(1, required=True),
    body=messages.StringField(2, required=True),
    tags=messages.StringField(3, repeated=True),
    author=messages.StringField(4, required=True))


@endpoints.api(name='blog', version='v1')
class BlogApi(remote.Service):
    """Blog API"""

    # Todo: create blog entry
    # Todo: passowrd hashing (utils function)
    # Todo: check if logged in (decorator!)
    @endpoints.method(request_message=NEW_AUTHOR_REQUEST,
        response_message=StringMessage,
        path='create_author',
        name='create_author',
        http_method='POST')
    def create_author(self, request):
        # Todo: create_author documentation
        # Todo: create_author error handling

        # Create an author
        password = generate_password(request.password)
        author = Author(user_name=request.user_name,
            email_address=request.email_address,
            password=password)
        author.put()

        return StringMessage(message="Worked")


    @endpoints.method(request_message=NEW_BLOG_ENTRY_REQUEST,
        response_message=StringMessage,
        path='create_blog_entry',
        name='create_blog_entry',
        http_method='POST')
    def create_blog_entry(self, request):
        # Todo: documentation
        # Todo: error handling

        # Todo: Create a blog post
        # Todo: get author function
        author = get_author(request.author)
        logger.debug(author)

        entry = BlogEntry()
        entry.title = request.title
        entry.body = request.body
        entry.author = author.key
        entry.tags = request.tags

        entry.put();

        return StringMessage(message="Worked")

    # @endpoints.method(request_message=NEW_PLAYER_REQUEST,
    #                   response_message=StringMessage,
    #                   path='register',
    #                   name='create_player',
    #                   http_method='POST')
    # def create_player(self, request):
    #     """Creates a new player.

    #     This function creates a new player. It will also make sure
    #     that the chosen username is not yet taken.
    #     (NB: Currently this function does not implement any validity checks
    #     on the email address, such as a regex etc.)

    #     Returns:
    #         StringMessage -- confirmation of player creation

    #     Raises:
    #         ConflictException -- if username or email address is taken already
    #     """
    #     # Check username and email address for conflicts
    #     if Player.query(Player.email_address == request.email_address).get():
    #         raise endpoints.ConflictException(
    #                 'A Player with that email address already exists.')
    #     if Player.query(Player.user_name == request.user_name).get():
    #         raise endpoints.ConflictException(
    #                 'A Player with that name already exists.')

    #     # Create player
    #     player = Player(user_name=request.user_name,
    #                     email_address=request.email_address)
    #     player.put()

    #     # Return confirmation of player creation
    #     return StringMessage(message='Player successfully created.')

    # @endpoints.method(request_message=NEW_GAME_REQUEST,
    #                   response_message=GameForm,
    #                   path='game/create_game',
    #                   name='create_game',
    #                   http_method='POST')
    # def create_game(self, request):
    #     """ Creates a new game.

    #     This function creates a new game.
    #     (NB: Games are just shells for questions. See the supplied readme
    #     for more information.)

    #     Returns:
    #         GameForm -- a GameForm representation of the created game
    #     """
    #     # Get player by username
    #     player = get_player(request.user_name)

    #     # Create the game
    #     game = Game.create_game(player=player.key, title=request.title)

    #     # Return confirmation of game creation
    #     return game.to_form()

    # @endpoints.method(request_message=NEW_MATCH_REQUEST,
    #                   response_message=MatchForm,
    #                   path='game/{urlsafe_game_key}/create_match',
    #                   name='create_match',
    #                   http_method='POST')
    # def create_match(self, request):
    #     """ Creates a new match.

    #     This match allows players to create a new match. A match is an
    #     'instance' of a game. This allows multiple users to play the same
    #     game at the same time or different times.


    #     Returns:
    #         StringMessage -- a confirmation that the match has been created

    #     Raises:
    #         BadRequestException -- raised when game has no questions or when
    #                                game is not in play mode or when play mode
    #                                enabling is required, but was not requested
    #     """
    #     # Get game and player from datastore
    #     game = get_by_urlsafe(request.urlsafe_game_key, Game)
    #     player = get_player(request.user_name)

    #     # Check if game has questions. A game with no questions is not playable
    #     if game.questions == []:
    #         raise endpoints.BadRequestException(
    #             'The game has no questions yet and cannot be played.')

    #     # Check if game has been changed from editing to play mode
    #     if not game.play_mode:
    #         # Only game creators can put a game into play mode
    #         if player.key != game.creator:
    #             raise endpoints.BadRequestException(
    #                 'Only the game creator can put it into play mode.')
    #         else:
    #             # Check if creator has explicitly requested to start the game
    #             if not request.start_game:
    #                 raise endpoints.BadRequestException(
    #                     'Play mode enabling was not requested.')
    #             else:
    #                 # Put game into play mode and save the change
    #                 game.play_mode = True
    #                 game.put()

    #     # Create the match
    #     match = Match.create_match(player=player.key, game=game)

    #     # Return a confirmation of the match creation
    #     return match.to_form()

    # @endpoints.method(request_message=LIST_REQUEST,
    #                   response_message=GameForms,
    #                   path='player/{user_name}/games',
    #                   name='get_user_games',
    #                   http_method='GET')
    # def get_user_games(self, request):
    #     """ Lists a player's games.

    #     This functions delivers a list of games by a specific player. It
    #     also allows pagination.
    #     (NB: Change QUERY_LIMIT to increase/decrease results per page)

    #     Returns:
    #         GamesForms -- a list of games in GameForm representation
    #     """
    #     # Get limit and offset based on requested page
    #     limit, offset = get_limit_offset(request.page)

    #     # Get the specified player's games
    #     player = get_player(request.user_name)
    #     games = Game.query(ancestor=player.key).fetch(offset=offset,
    #                                                   limit=limit)
    #     games = [game.to_form() for game in games]

    #     # Return games
    #     return GameForms(games=games)

    # @endpoints.method(request_message=LIST_REQUEST,
    #                   response_message=MatchForms,
    #                   path='player/{user_name}/matches',
    #                   name='get_user_matches',
    #                   http_method='GET')
    # def get_user_matches(self, request):
    #     """ Lists a player's matches.

    #     This functions delivers a list of matches by a specific player. It
    #     also allows pagination.
    #     (NB: Change QUERY_LIMIT to increase/decrease results per page)

    #     Returns:
    #         MatchForms -- a list of matches in MatchForm representation
    #     """
    #     # Get limit and offset based on requested page
    #     limit, offset = get_limit_offset(request.page)

    #     # Get the specified player's matches
    #     player = get_player(request.user_name)
    #     matches = Match.query(ancestor=player.key).fetch(offset=offset,
    #                                                      limit=limit)
    #     matches = [match.to_form() for match in matches]

    #     # Return matches
    #     return MatchForms(matches=matches)

    # @endpoints.method(request_message=LIST_REQUEST,
    #                   response_message=ScoreForms,
    #                   path='high_scores',
    #                   name='get_high_scores',
    #                   http_method='GET')
    # def get_high_scores(self, request):
    #     """ Lists players' scores.

    #     This functions delivers a player list ordered by their scores. It
    #     also allows pagination.
    #     (NB: Change QUERY_LIMIT to increase/decrease results per page)

    #     Returns:
    #         ScoreForms -- a list of scores in ScoreForm representation
    #     """
    #     # Get limit and offset based on requested page
    #     limit, offset = get_limit_offset(request.page)

    #     # Get the players' scores
    #     players = Player.query().order(-Player.score).fetch(offset=offset,
    #                                                         limit=limit)
    #     scores = [player.to_scoreform() for player in players]

    #     # Return scores
    #     return ScoreForms(scores=scores)

    # @endpoints.method(request_message=GET_ENTITY_REQUEST,
    #                   response_message=StringMessage,
    #                   path='match/{urlsafe_key}/cancel_match',
    #                   name='cancel_match',
    #                   http_method='DELETE')
    # def cancel_match(self, request):
    #     """ Deletes a match.

    #     This function allows players to cancel their own (and only their own)
    #     matches. Cancelled matches are deleted and cannot be recovered.
    #     Only unfinished matches can be deleted.

    #     Returns:
    #         StringMessage -- a confirmation of the match deletion

    #     Raises:
    #         ForbiddenException -- raised if a player tries to
    #                               delete another player's match
    #                               or if the match does not exist
    #     """
    #     # Get the specified match
    #     match = get_by_urlsafe(request.urlsafe_key, Match)

    #     # Check whether match exists, if not throw error
    #     if not match:
    #         raise endpoints.ForbiddenException('Match does not exist.')

    #     # Check deletion request comes from the creator of the match
    #     player = get_player(request.user_name)
    #     if match and match.player != player.key:
    #         raise endpoints.ForbiddenException(
    #             'You cannot delete other players\'s matches.')

    #     # Check whether match has already finished
    #     if match.match_over:
    #         raise endpoints.ForbiddenException(
    #             'You cannot delete a finished match.')

    #     # Delete the match
    #     match.key.delete()

    #     # Return confirmation of match deletion
    #     return StringMessage(message='Your match was successfully deleted.')

    # @endpoints.method(request_message=NEW_QUESTION_REQUEST,
    #                   response_message=QuestionForm,
    #                   path='question/create_question',
    #                   name='create_question',
    #                   http_method='POST')
    # def create_question(self, request):
    #     """ Allows players to create questions.

    #     This function allows players to create questions.

    #     Returns:
    #         QuestionForm -- QuestionForm representation of the created question
    #     """
    #     # Construct a question from the request
    #     question = Question(question=request.question,
    #                         incorrect_answers=request.incorrect_answers,
    #                         correct_answer=request.correct_answer)
    #     key = question.put()
    #     logger.debug("Question successfully created.")

    #     # If a game key has been provided, add the question to the game
    #     if request.urlsafe_game_key is not None:
    #         game = get_by_urlsafe(request.urlsafe_game_key, Game)
    #         game.questions.append(key)
    #         game.put()
    #         logger.debug("Question added to game.")

    #     # Return confirmation of question creation and/or added to a game
    #     return question.to_form()

    # @endpoints.method(request_message=QUESTION_GAME_REQUEST,
    #                   response_message=StringMessage,
    #                   path='game/{urlsafe_game_key}/add_question',
    #                   name='add_question',
    #                   http_method='POST')
    # def add_question(self, request):
    #     """ Allows players to add questions to existing games.

    #     This function allows players to add already existing questions to
    #     existing games. This allows questions to be re-used across many games
    #     rather than belong to one game only.
    #     (NB: This does not create a new questions, just allows questions from
    #     one game to be used in another. To create new questions use the
    #     create_question endpoints method)

    #     Returns:
    #         StringMessage -- A confirmation that the question has been
    #                          successfully added to a game
    #     """
    #     # Get game and question from datastore
    #     game = get_by_urlsafe(request.urlsafe_game_key, Game)
    #     question = get_by_urlsafe(request.urlsafe_question_key, Question)

    #     # Add the question to the game and save the changes
    #     game.questions.append(question.key)
    #     game.put()

    #     # Return confirmation that question has been added to game
    #     return StringMessage(message="Question successfully added to Game")

    # @endpoints.method(request_message=GET_ENTITY_REQUEST,
    #                   response_message=StringMessage,
    #                   path='game/{urlsafe_key}/set_playmode',
    #                   name='set_playmode',
    #                   http_method='POST')
    # def set_playmode(self, request):
    #     """ Set a game's play mode

    #     This function allows to put a game into play mode. Games in play mode
    #     allow the creation of matches which players can then play.
    #     (NB: Only game creators may put a game into play mode)

    #     Returns:
    #         StringMessage -- a confirmation that the play mode is enabled

    #     Raises:
    #         ForbiddenException -- raised if player requesting play mode is not
    #                               the game's creator or the game does not exist
    #         BadRequestException -- raised when the user has not explicitly
    #                                requested the game be put into play mode
    #     """
    #     # Get the game and player from the datastore
    #     game = get_by_urlsafe(request.urlsafe_key, Game)
    #     player = get_player(request.user_name)

    #     if not game:
    #         raise endpoints.ForbiddenException(
    #             'The game does not exist.')

    #     if game.questions == []:
    #         raise endpoints.BadRequestException(
    #             'The game has no questions and cannot be played.')

    #     # Only game creators can put a game into play mode
    #     if player.key != game.creator:
    #         raise endpoints.ForbiddenException(
    #             'Only the game creator can put it into play mode.')
    #     else:
    #         # Check if creator has explicitly requested to start the game
    #         if not request.start_game:
    #             raise endpoints.BadRequestException(
    #                 'Play mode enabling was not requested.')
    #         else:
    #             # Put game into play mode and save the change
    #             game.play_mode = True
    #             game.put()

    #     # Return confirmation that play mode is now enabled
    #     return StringMessage(message="Game is now in play mode.")

    # @endpoints.method(request_message=GET_ENTITY_REQUEST,
    #                   response_message=MatchForm,
    #                   path='match/{urlsafe_key}/history',
    #                   name='get_match_history',
    #                   http_method='GET')
    # def get_match_history(self, request):
    #     """ Retrieves a game's history.

    #     This function allows players to see the history of their matches.
    #     Players are only allowed to view the history of their own matches;
    #     access to other player's history is not granted.

    #     Returns:
    #         MatchForm -- the match details including the history

    #     Raises:
    #         ForbiddenException -- raised when an attempt is made to view
    #                               another player's history
    #     """
    #     # Get the requested match and player from the datastore
    #     match = get_by_urlsafe(request.urlsafe_key, Match)
    #     player = get_player(request.user_name)

    #     # If match player and request player do not match, deny history access
    #     if match.player != player.key:
    #         raise endpoints.ForbiddenException(
    #             'You may not view another player\'s history')

    #     # Return history as part of a MatchForm representation
    #     return match.to_form(history=True)

    # @endpoints.method(request_message=GET_QUESTION_REQUEST,
    #                   response_message=QuestionForm,
    #                   path='match/{urlsafe_match_key}/get_question',
    #                   name='get_question',
    #                   http_method='GET')
    # def get_question(self, request):
    #     """ Retrieves a question.

    #     This function gets a question from the datastore and returns it
    #     as a QuestionForm representation. Specifically it gets and delivers
    #     the match's current round's question.

    #     Returns:
    #         QuestionForm -- a QuestionForm representation of the question

    #     Raises:
    #         ForbiddenException -- raised if the match has finished, i.e. there
    #                               are no more questions left in the match (and)
    #                               thus cannot be retrieved from the datastore
    #     """
    #     # Get the requested match from the datastore
    #     match = get_by_urlsafe(request.urlsafe_match_key, Match)

    #     # If the match is over, no more questions can be retrieved
    #     if match.match_over:
    #         raise endpoints.ForbiddenException(
    #             'Match has been closed, there are no more questions left.')

    #     # Get the match's current round's question from the datastore
    #     question = match.questions[match.current_round].get()

    #     # Return the question in a QuestionForm representation
    #     return question.to_form()

    # @endpoints.method(request_message=PROFILE_REQUEST,
    #                   response_message=ProfileForm,
    #                   path='player/{user_name}/profile',
    #                   name='get_player_profile',
    #                   http_method='GET')
    # def get_player_profile(self, request):
    #     """ Retrieves a player's profile.

    #     This function retrieves a player's profile.

    #     Returns:
    #         ProfileForm -- the player's public profile as a ProfileForm
    #     """
    #     # Retrieve player from datastore
    #     player = get_player(request.user_name)

    #     # Return ProfileForm representation of player
    #     return player.to_profileform()

    # @endpoints.method(request_message=PROFILE_REQUEST,
    #                   response_message=ScoreForm,
    #                   path='player/{user_name}/ranking',
    #                   name='get_user_ranking',
    #                   http_method='GET')
    # def get_user_ranking(self, request):
    #     """ Get a player's ranking.

    #     This function serves no real purpose and was just included to fullfil
    #     the Udacity course project requirements. This information is also
    #     included in a player's profile (see get_player_profile).

    #     Returns:
    #         ScoreForm -- a player's ranking in ScoreForm representation
    #     """
    #     # Get player from datastore and return their ranking
    #     player = get_player(request.user_name)
    #     return ScoreForm(user_name=player.user_name,
    #                      batting_avg=player.batting_avg)

    # @endpoints.method(request_message=PROFILE_REQUEST,
    #                   response_message=ScoreForm,
    #                   path='player/{user_name}/score',
    #                   name='get_user_score',
    #                   http_method='GET')
    # def get_user_score(self, request):
    #     """ Get a player's score.

    #     This function serves no real purpose and was just included to fullfil
    #     the Udacity course project requirements. This information is also
    #     included in a player's profile (see get_player_profile).

    #     Returns:
    #         ScoreForm -- a player's score in ScoreForm representation
    #     """
    #     player = get_player(request.user_name)

    #     return ScoreForm(user_name=player.user_name,
    #                      score=player.score)

    # @endpoints.method(request_message=ANSWER_REQUEST,
    #                   response_message=AnswerMessage,
    #                   path='match/{urlsafe_match_key}/submit_answer',
    #                   name='submit_answer',
    #                   http_method='POST')
    # def submit_answer(self, request):
    #     """ Allows players to submit questions to answers

    #     This function allows players to submit answers to questions in a match.
    #     It will also make sure that the question being answered belongs to the
    #     current round. This counteracts the accidental submission of answers
    #     several times in a row.

    #     Returns:
    #         AnswerMessage -- information about whether the player has answered
    #                          the question correctly or incorrectly

    #     Raises:
    #         ForbbidenException -- raised if the match to which the answer was
    #                               submitted has finished already
    #         BadRequestException -- raised if the player tried to submit an
    #                                answer to a round which is not the match's
    #                                current round
    #     """
    #     # Get the match from the datastore
    #     match = get_by_urlsafe(request.urlsafe_match_key, Match)

    #     # Check if match is still ongoing
    #     if match.match_over:
    #         raise endpoints.ForbiddenException(
    #             'Match is over, answering is not possible.')

    #     # Check that answer submitted is for the current round
    #     if match.current_round != request.round:
    #         raise endpoints.BadRequestException(
    #             "That's not the right round.")

    #     # Get the question and the player info from the datastore
    #     question = get_by_urlsafe(request.urlsafe_question_key, Question)
    #     player = get_player(request.user_name)

    #     # Check if answer was correct
    #     if request.answer == question.correct_answer:
    #         logger.debug('Player has guessed correct answer.')
    #         correct_answer = True
    #         player.correct_answers += 1
    #     else:
    #         logger.debug('Player has guessed an incorrect answer.')
    #         correct_answer = False

    #     # V basic scoring system
    #     if correct_answer:
    #         match.score += 100

    #     # Increase number of questions answered by player
    #     # for v basic ranking system
    #     player.total_questions += 1

    #     # Add answer to the history
    #     history = History(question=question.question,
    #                       correct_answer=correct_answer,
    #                       answer=request.answer)
    #     match.history.append(history)

    #     # Advance one round
    #     # If last round is over transfer score to player and close the match
    #     match.current_round += 1
    #     logger.debug('New current round: %s' % match.current_round)
    #     if match.current_round == len(match.questions):
    #         match.match_over = True
    #     if match.match_over:
    #         player.score += match.score

    #     # Commit match and player changes to datastore
    #     player.put()
    #     match.put()

    #     # Return whether answer was answered correcty or incorrectly
    #     return AnswerMessage(correct_answer=correct_answer)


api = endpoints.api_server([BlogApi])
