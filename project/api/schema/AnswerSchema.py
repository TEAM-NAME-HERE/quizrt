from django.http import Http404

from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphene import relay, ObjectType, Mutation
from graphene.relay import Connection, ConnectionField
import graphene

from project.api.models import Answer, Question


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        filter_fields = ['description', 'question', 'is_correct', 'id']
        interfaces = (relay.Node, )


class AnswerInput(graphene.InputObjectType):
    description = graphene.String(required=True)
    question = graphene.String(required=True)
    is_correct = graphene.Boolean(required=True)


class CreateAnswer(relay.ClientIDMutation):
    class Input:
        answer_data = AnswerInput(required=True)

    answer = graphene.Field(AnswerNode)
    uuid = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        answer = Answer.objects.create(
            description=input['answer_data'].description,
            is_correct=input['answer_data'].is_correct,
            question=Question.objects.get(uuid=input['answer_data'].question)
        )
        return CreateAnswer(answer=answer, uuid=answer.uuid)


class UpdateAnswer(relay.ClientIDMutation):
    class Input:
        uuid = graphene.String(required=True)
        description = graphene.String(required=False)
        is_correct = graphene.Boolean(required=False)


    answer = graphene.Field(AnswerNode)
    uuid = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # TODO: only allow modification of items owned by user
        answer = Answer.objects.get(uuid=input['uuid'])
        if input['description']:
            answer.description = input['description']
        if input['is_correct']:
            answer.is_correct = input['is_correct']
        answer.save()
        return UpdateAnswer(answer=answer, uuid=answer.uuid)


class Query(graphene.AbstractType):
        answers = DjangoFilterConnectionField(AnswerNode)
        answer = relay.Node.Field(AnswerNode)


class Mutation(graphene.AbstractType):
    create_answer = CreateAnswer.Field()
    update_answer = UpdateAnswer.Field()
