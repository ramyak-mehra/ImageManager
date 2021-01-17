import graphene
import imagehandler.graphql.queries as image_queries
import imagehandler.graphql.mutations as image_mutations
import utility.auth_mutations as auth_mutations


class Query(image_queries.Query, graphene.ObjectType):
    pass


class Mutation(image_mutations.Mutation, auth_mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
