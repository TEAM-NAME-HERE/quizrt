from operator import itemgetter, attrgetter, methodcaller

from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
from graphql_relay import from_global_id
import graphene
from functools import reduce 

from project.api.models import QuizSession, User, Quiz, Question

class SessionNode(DjangoObjectType):
    class Meta:
        model = QuizSession
        filter_fields = ['owner', 'quiz', 'is_locked']
        interfaces = (relay.Node, )


# class SessionInput(graphene.InputObjectType):
#     owner = graphene.ID(required=True)
#     quiz = graphene.ID(required=True)


class CreateSession(relay.ClientIDMutation):
    class Input:
        # session_data = SessionInput(required=True)
        owner = graphene.ID(required=True)
        quiz = graphene.ID(required=True)

    session = graphene.Field(SessionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user_ID = from_global_id(input.get('owner')) 
        quiz_ID = from_global_id(input.get('quiz')) 
        kwargs = {
            "owner": User.objects.get(pk=user_ID[1]),
            "quiz": Quiz.objects.get(pk=quiz_ID[1]),
        }
        session = QuizSession.objects.create(**kwargs)
        session.save()
        return CreateSession(session=session)


class DeleteSession(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input.get('id'))
        try:
            session = QuizSession.objects.get(pk=rid[1])
            session.delete()
            return DeleteSession(success=True)
        except QuizSession.DoesNotExist:
            raise Exception('404 Not Found')


class CloseSession(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        # is_locked = graphene.Boolean(required=False)

    session = graphene.Field(SessionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input.get('id'))
        session = QuizSession.objects.get(pk=rid[1])
        # if(input['is_locked']):
        #     session.is_locked = input['is_locked']
        session.is_locked = True
        session.save()
        return CloseSession(session=session)


class DisplayResults(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    session = graphene.Field(SessionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input.get('id'))
        session = QuizSession.objects.get(pk=rid[1])
        session.display_results = True
        session.save()
        return DisplayResults(session=session)


class AdvanceQuestion(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    session = graphene.Field(SessionNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        rid = from_global_id(input.get('id'))
        session = QuizSession.objects.get(pk=rid[1])
        if session.current_question is None:
            # Find question with minimum order number and set it to current_question
            min_order = None
            first_question = reduce(lambda a,b: a if a.order_number < b.order_number else b,
                                    session.quiz.question_set.all())
            print(first_question)
            # for question in session.quiz.question_set.all():
            #     if min_order is None:
            #         min_order = question.order_number
            #         first_question = question
            #     elif question.order_number < min_order:
            #         min_order = question.order_number
            #         first_question = question
            session.current_question = first_question
            session.save()
            return AdvanceQuestion(session=session)

        # Find the question closest to the current question (based on the order number)
        curr_question_order = session.current_question.order_number
        min_order_diff = None
        for question in session.quiz.question_set.all():
            order_diff = question.order_number - curr_question_order
            if (order_diff > 0) and (min_order_diff is None):
                min_order_diff = order_diff
            elif (order_diff > 0) and (order_diff < min_order_diff):
                min_order_diff = order_diff
        # the session is over (no more questions)
        if min_order_diff is None:
            session.current_question = None
            session.display_results = False
            session.is_locked = True
            session.save()
            return AdvanceQuestion(session=session)
        else:
            # sets the current question field to be the found question
            next_order_num = curr_question_order + min_order_diff
            next_question = Question.objects.filter(order_number=next_order_num, quiz=session.quiz)[0]
            session.current_question = next_question
            session.display_results = False
            session.save()
            return AdvanceQuestion(session=session)


class UserScore(graphene.ObjectType):
    username = graphene.String(required=True)
    score = graphene.Int(required=True)


class Query(object):
    sessions = DjangoFilterConnectionField(SessionNode)
    session = relay.Node.Field(SessionNode)
    user_scores = graphene.Field(graphene.NonNull(graphene.List(UserScore)), id=graphene.ID(required=True))
    
    def resolve_user_scores(self, info, **kwargs):
        rid = from_global_id(kwargs.get('id'))
        if rid is None:
            return None
        session = QuizSession.objects.get(pk=rid[1])
        user_scores = {}
        short_list = session.response_set.distinct('user')
        for user in short_list:
            user_scores[user.user] = 0
        for response in session.response_set.all():
            user_scores[response.user] += response.get_score()

        sorted_scores = sorted(user_scores.items(), key=itemgetter(1), reverse=True)
        scores = []
        for s in sorted_scores:
            ss = UserScore(username = s[0], score = s[1])
            scores.append(ss)
        return scores


class Mutation(object):
    create_session = CreateSession.Field()
    delete_session = DeleteSession.Field()
    close_session = CloseSession.Field()
    display_results = DisplayResults.Field()
    advance_question = AdvanceQuestion.Field()