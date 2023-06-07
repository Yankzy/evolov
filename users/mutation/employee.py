import graphene
from users.models import Employee, Company
from users.types import EmployeeType, UserType, CompanyType
from graphql.error import GraphQLError

class ToggleEmployeeStatus(graphene.Mutation):
    class Arguments:
        employee_id = graphene.ID()

    employee = graphene.Field(Employee)

    def mutate(self, info, employee_id):
        employee = Employee.objects.get(pk=employee_id)
        employee.is_active = not employee.is_active
        employee.save()
        return ToggleEmployeeStatus(employee=employee)


class ShowEmployees(graphene.Mutation):
    to_return = graphene.Field(CompanyType)

    class Arguments:
        event_type = graphene.String(required=True)
        company_id = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        if kwargs.get('event_type') != 'show_employees':
            raise GraphQLError("Wrong event_type")
        
        company = Company.objects.get(pk=kwargs['company_id'])

        company.show_employees = not company.show_employees
        company.save()
        return ShowEmployees(to_return=company)


class EmployeeMutations(graphene.ObjectType):
    # toggle_employee_status = ToggleEmployeeStatus.Field()
    show_employees = ShowEmployees.Field()