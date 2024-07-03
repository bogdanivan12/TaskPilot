"""Populate the database with dummy data"""
import requests

from taskpilot.common import config_info, api_request_classes as api_req

CREATE_USER_REQUESTS = [
    api_req.CreateUserRequest(
        username="bogdanivan",
        email="bogdan.ivan@s.unibuc.ro",
        full_name="Bogdan Ivan",
        password="Bogdan123!"
    ),
    api_req.CreateUserRequest(
        username="admin",
        email="admin@taskpilot.com",
        full_name="Admin TaskPilot",
        password="Admin123!",
        is_admin=True
    ),
    api_req.CreateUserRequest(
        username="alsandu",
        email="alsandu@gmail.com",
        full_name="Alexandru Sandu",
        password="Alex123!"
    ),
    api_req.CreateUserRequest(
        username="againa",
        email="againa@taskpilot.com",
        full_name="Aurelian-Octavian Gaina",
        password="Gaina123!"
    ),
    api_req.CreateUserRequest(
        username="mateiionescu",
        email="mateiit2002@gmail.com",
        full_name="Matei-Daniel Ionescu",
        password="Matei123!"
    )
]

CREATE_PROJECT_REQUESTS = [
    api_req.CreateProjectRequest(
        project_id="TaskPilot",
        title="TaskPilot",
        description="Platforma de management al proiectelor orientata pe"
                    " lucrul la distanta, cu functionalitati de asistent"
                    " virtual ce joaca rolul de manager de proiect.",
        created_by="bogdanivan",
        members=["alsandu", "bogdanivan"]
    ),
    api_req.CreateProjectRequest(
        project_id="APIGEN",
        title="API Generator",
        description="O solutie software care genereaza automat endpoint-uri"
                    " API pe baza unor script-uri si a unor fisiere de"
                    " configurare.",
        created_by="alsandu",
        members=["bogdanivan", "alsandu", "againa", "mateiionescu"]
    )
]

CREATE_TASK_REQUESTS = [
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-0",
        title="Analiza solutiei",
        description="In calitate de owner al proiectului TaskPilot, vreau sa"
                    " analizez solutia pentru a putea incepe implementarea",
        type="Story",
        priority="Critical",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-1",
        title="Dezvoltarea API-ului",
        description="Pentru a putea implementa functionalitatile de baza ale"
                    " aplicatiei, trebuie dezvoltata componenta backend."
                    " Aceasta va fi realizata sub forma unui API de tip REST"
                    " care va fi folosit de catre componenta frontend. API-ul"
                    " va fi realizat in limbajul Python folosind framework-ul"
                    " FastAPI si va expune endpoint-uri ce vor acoperi logica"
                    " de business a aplicatiei.",
        type="Epic",
        priority="Normal",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-2",
        title="Dezvoltarea UI-ului",
        description="Pentru a putea implementa functionalitatile de baza ale"
                    " aplicatiei, trebuie dezvoltata componenta frontend."
                    " Aceasta va fi realizata folosind limbajul Python si"
                    " framework-ul NiceGUI si va comunica cu API-ul backend."
                    " Interfata va fi simpla si intuitiva, cu un design placut"
                    " si usor de folosit.",
        type="Epic",
        priority="Normal",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-3",
        title="Dezvoltarea bazei de date",
        description="Pentru a putea implementa functionalitatile de baza ale"
                    " aplicatiei, trebuie dezvoltata baza de date. Aceasta va"
                    " fi reprezentata sub forma unei baze de date"
                    " non-relationale (NoSQL) si va fi realizata folosind"
                    " tehnologia Elasticsearch.",
        type="Epic",
        priority="High",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-4",
        title="Dezvoltarea modelelor de date",
        description="In calitate de developer, vreau sa dezvolt modelele de"
                    " date pentru a putea realiza interactiunea cu baza de"
                    " date Elasticsearch.",
        type="Story",
        priority="High",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-3",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-5",
        title="Containerizarea Elasticsearch",
        description="In calitate de developer, vreau sa creez un container"
                    " Docker pentru Elasticsearch pentru a putea rula baza de"
                    " date pe orice sistem de operare.",
        type="Story",
        priority="High",
        status="Closed",
        created_by="alsandu",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-3",
        assignee="alsandu"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-6",
        title="Crearea claselor corespunzatoare modelelor de date",
        description="Pentru a putea realiza interactiunea cu baza de date"
                    " Elasticsearch, trebuie create clasele corespunzatoare"
                    " modelelor de date.",
        type="Task",
        priority="High",
        status="Closed",
        created_by="alsandu",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-4",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-7",
        title="Crearea fisierului de tip Dockerfile",
        description="Pentru a putea crea containerul Docker pentru"
                    " Elasticsearch, trebuie creat fisierul de tip Dockerfile"
                    " care va contine instructiunile necesare pentru"
                    " containerizare.",
        type="Task",
        priority="Low",
        status="Closed",
        created_by="alsandu",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-5",
        assignee="alsandu"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-8",
        title="Rularea containerului Elasticsearch",
        description="Pentru a putea rula containerul Docker pentru"
                    " Elasticsearch, trebuie construita imaginea pe baza"
                    " fisierului Dockerfile si apoi rulata.",
        type="Task",
        priority="Low",
        status="Closed",
        created_by="alsandu",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-5",
        assignee="alsandu"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-9",
        title="CRUD pe modelele de date",
        description="In calitate de utilizator, imi doresc sa pot crea, citi,"
                    " actualiza si sterge date din baza de date Elasticsearch"
                    " pentru a putea interactiona cu aplicatia.",
        type="Story",
        priority="High",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-1",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-10",
        title="CRUD pe clasa Project",
        description="Pentru a putea interactiona cu proiectele din baza de"
                    " date, trebuie realizate operatiile de tip"
                    " CRUD pe clasa Project.",
        type="Task",
        priority="Normal",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-9",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-11",
        title="CRUD pe clasa Ticket",
        description="Pentru a putea interactiona cu ticketele din baza de"
                    " date, trebuie realizate operatiile de tip"
                    " CRUD pe clasa Ticket.",
        type="Task",
        priority="Normal",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-9",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-12",
        title="CRUD pe clasa User",
        description="Pentru a putea interactiona cu utilizatorii din baza de"
                    " date, trebuie realizate operatiile de tip"
                    " CRUD pe clasa User.",
        type="Task",
        priority="Normal",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-9",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-13",
        title="CRUD pe clasa Comment",
        description="Pentru a putea interactiona cu comentariile din baza de"
                    " date, trebuie realizate operatiile de tip"
                    " CRUD pe clasa Comment.",
        type="Task",
        priority="Normal",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-9",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-14",
        title="Implementarea functionalitatii AI",
        description="In calitate de utilizator, imi doresc sa pot interactiona"
                    " cu un asistent virtual care sa imi ofere informatii"
                    " despre proiecte si task-uri.",
        type="Story",
        priority="Normal",
        status="In Progress",
        created_by="alsandu",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-1",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-15",
        title="Interactiunea cu GPT-4o",
        description="Pentru a putea implementa interactiunea cu asistentul"
                    " virtual, trebuie realizata integrarea cu modelul de"
                    " generare a limbajului natural GPT-4o.",
        type="Task",
        priority="Normal",
        status="In Progress",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-14",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-16",
        title="Dezvoltarea sistemului de autentificare",
        description="In calitate de owner al proiectului TaskPilot, vreau sa"
                    " pot autentifica si autoriza utilizatorii in aplicatie"
                    " pentru a putea interactiona cu aceasta si pentru a avea"
                    " acces la toate datele necesare.",
        type="Story",
        priority="Low",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-2",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-17",
        title="Dezvoltarea paginilor de autentificare si inregistrare",
        description="Pentru a putea utilizatorii sa interactioneze cu"
                    " aplicatia, trebuie realizate paginile de autentificare"
                    " si inregistrare.",
        type="Task",
        priority="Low",
        status="Not Started",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-16",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-18",
        title="Dezvoltarea mecanismului de autentificare",
        description="Pentru a putea utilizatorii sa interactioneze cu"
                    " aplicatia, trebuie realizat mecanismul de"
                    " autentificare.",
        type="Task",
        priority="Low",
        status="Not Started",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-16",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-19",
        title="Dezvoltarea mecanismului de autorizare",
        description="Pentru a putea utilizatorii sa interactioneze cu"
                    " aplicatia, trebuie realizat mecanismul de autorizare.",
        type="Task",
        priority="Low",
        status="Not Started",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-16",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-20",
        title="Dezvoltarea paginilor modelelor de date",
        description="In calitate de utilizator, imi doresc sa pot interactiona"
                    " cu modelele de date pentru a putea folosi platforma"
                    " TaskPilot in scopul de a imi organiza proiectele.",
        type="Story",
        priority="Normal",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-2",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-21",
        title="Dezvoltarea paginilor de proiect",
        description="Pentru a putea utilizatorii sa interactioneze cu"
                    " proiectele, trebuie realizate paginile de proiect.",
        type="Task",
        priority="Normal",
        status="Not Started",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-20",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-22",
        title="Dezvoltarea paginilor de ticket",
        description="Pentru a putea utilizatorii sa interactioneze cu"
                    " ticketele, trebuie realizate paginile de ticket.",
        type="Task",
        priority="Normal",
        status="Not Started",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-20",
        assignee="bogdanivan"
    ),
    api_req.CreateTicketRequest(
        ticket_id="TaskPilot-23",
        title="Tipuri de utilizatori",
        description="Pentru a putea analiza solutia propusa trebuie"
                    " identificate tipurile de utilizatori",
        type="Task",
        priority="Normal",
        status="Closed",
        created_by="bogdanivan",
        parent_project="TaskPilot",
        parent_ticket="TaskPilot-0",
        assignee="bogdanivan"
    ),

    api_req.CreateTicketRequest(
        ticket_id="APIGEN-0",
        title="Crearea template-urilor",
        description="In calitate de dezvoltator, vreau sa creez template-uri"
                    " pentru generarea de cod, pentru a avea o solutie"
                    " standardizata.",
        type="Story",
        priority="Normal",
        status="In Progress",
        created_by="alsandu",
        parent_project="APIGEN",
        assignee="againa"
    ),
    api_req.CreateTicketRequest(
        ticket_id="APIGEN-1",
        title="Crearea template-urilor pentru endpoint-uri",
        description="Pentru a putea genera endpoint-uri API, trebuie create"
                    " template-uri pentru acestea.",
        type="Task",
        priority="Normal",
        status="In Progress",
        created_by="againa",
        parent_project="APIGEN",
        parent_ticket="APIGEN-0",
        assignee="againa"
    ),
    api_req.CreateTicketRequest(
        ticket_id="APIGEN-2",
        title="Crearea template-urilor pentru clasele de request",
        description="Pentru a putea genera endpoint-uri API, trebuie create"
                    " template-uri pentru clasele de request.",
        type="Task",
        priority="Normal",
        status="In Progress",
        created_by="againa",
        parent_project="APIGEN",
        parent_ticket="APIGEN-0",
        assignee="againa"
    ),
    api_req.CreateTicketRequest(
        ticket_id="APIGEN-3",
        title="Crearea template-urilor pentru clasele de raspuns",
        description="Pentru a putea genera endpoint-uri API, trebuie create"
                    " template-uri pentru clasele de raspuns.",
        type="Task",
        priority="Normal",
        status="In Progress",
        created_by="againa",
        parent_project="APIGEN",
        parent_ticket="APIGEN-0",
        assignee="againa"
    ),
    api_req.CreateTicketRequest(
        ticket_id="APIGEN-4",
        title="Crearea template-urilor pentru fisierele de configurare",
        description="Pentru a putea genera endpoint-uri API, trebuie create"
                    " template-uri pentru fisierele de configurare.",
        type="Task",
        priority="Normal",
        status="In Progress",
        created_by="againa",
        parent_project="APIGEN",
        parent_ticket="APIGEN-0",
        assignee="againa"
    ),
    api_req.CreateTicketRequest(
        ticket_id="APIGEN-5",
        title="Crearea mecanismului de generare de endpoint",
        description="In calitate de inginer operational in infrastructura, imi"
                    " doresc sa pot genera endpoint-uri API pe baza"
                    " script-urilor dezvoltate de mine, pentru a putea"
                    " contribui la API-urile dezvoltate de colegii mei"
                    " developeri.",
        type="Story",
        priority="Normal",
        status="In Progress",
        created_by="alsandu",
        parent_project="APIGEN",
        assignee="mateiionescu"
    ),
    api_req.CreateTicketRequest(
        ticket_id="APIGEN-6",
        title="Generarea codului pentru endpoint",
        description="Pentru a putea crea endpoint-ul pe baza scriptului, este"
                    " nevoie de generarea codului pentru functia endpoint pe"
                    " baza template-urilor definite.",
        type="Task",
        priority="Normal",
        status="Not Started",
        created_by="mateiionescu",
        parent_project="APIGEN",
        parent_ticket="APIGEN-5",
        assignee="mateiionescu"
    ),
    api_req.CreateTicketRequest(
        ticket_id="APIGEN-7",
        title="Rularea unui script efemer",
        description="Pentru a putea crea endpoint-ul pe baza scriptului, este"
                    " nevoie de ca functia endpoint generata sa ruleze un"
                    " script efemer, ce nu va lasa in urme informatii"
                    " sensibile",
        type="Task",
        priority="Normal",
        status="Not Started",
        created_by="mateiionescu",
        parent_project="APIGEN",
        parent_ticket="APIGEN-5",
        assignee="bogdanivan"
    ),
]

CREATE_COMMENT_REQUESTS = [
    api_req.CreateCommentRequest(
        comment_id="TaskPilot-0-0",
        ticket_id="TaskPilot-0",
        text="Tipurile de utilizatori sunt membrii echipelor si managerii de"
             " proiect.",
        created_by="bogdanivan"
    ),
    api_req.CreateCommentRequest(
        comment_id="TaskPilot-1-0",
        ticket_id="TaskPilot-1",
        text="Pot face eu task-urile din acest epic.",
        created_by="bogdanivan"
    ),
    api_req.CreateCommentRequest(
        comment_id="TaskPilot-9-0",
        ticket_id="TaskPilot-9",
        text="Au fost create functii generale pentru operatiile CRUD pe baza"
             " de date, ce primesc ca parametru indexul asociat clasei.",
        created_by="bogdanivan"
    ),
    api_req.CreateCommentRequest(
        comment_id="TaskPilot-15-0",
        ticket_id="TaskPilot-15",
        text="A fost creat un modul separat, la nivelul package-ului common,"
             " ce se ocupa de interactiunea cu OpenAI API. Functia principala"
             " contine parametri ce permit adaugarea de chat history pentru"
             " persistenta mesajelor.",
        created_by="bogdanivan"
    ),

    api_req.CreateCommentRequest(
        comment_id="APIGEN-0-0",
        ticket_id="APIGEN-0",
        text="Pentru crearea template-urilor se vor folosi Jinja templates,"
             " pentru a avea o solutie standardizata.",
        created_by="againa"
    ),
    api_req.CreateCommentRequest(
        comment_id="APIGEN-7-0",
        ticket_id="APIGEN-7",
        text="Script-urile vor fi template-izate, clonate si populate cu"
             " datele necesare. Dupa rularea lor si intoarcerea raspunsului,"
             " acestea vor fi sterse.",
        created_by="bogdanivan"
    ),
    api_req.CreateCommentRequest(
        comment_id="APIGEN-7-1",
        ticket_id="APIGEN-7",
        text="Suna bine, dar trebuie sa avem grija sa nu lasam date sensibile"
             " in loguri.",
        created_by="mateiionescu"
    ),
]


def create_users():
    """Create users"""
    url = (
        f"http://{config_info.HOST}:{config_info.API_PORT}"
        f"/{config_info.API_ROUTES[config_info.APIOperations.USERS_CREATE]}"
    )
    for request in CREATE_USER_REQUESTS:
        response = requests.post(
            url=url,
            json=request.dict()
        )
        print(f"[{response.json()['result']}] Create User Response for request"
              f" {request}: {response.json()}")


def create_projects():
    """Create projects"""
    url = (
        f"http://{config_info.HOST}:{config_info.API_PORT}"
        f"/{config_info.API_ROUTES[config_info.APIOperations.PROJECTS_CREATE]}"
    )
    for request in CREATE_PROJECT_REQUESTS:
        response = requests.post(
            url=url,
            json=request.dict()
        )
        print(f"[{response.json()['result']}] Create Project Response for"
              f" request {request}: {response.json()}")


def create_tasks():
    """Create tasks"""
    url = (
        f"http://{config_info.HOST}:{config_info.API_PORT}"
        f"/{config_info.API_ROUTES[config_info.APIOperations.TICKETS_CREATE]}"
    )
    for request in CREATE_TASK_REQUESTS:
        response = requests.post(
            url=url,
            json=request.dict()
        )
        print(f"[{response.json()['result']}] Create Task Response for request"
              f" {request}: {response.json()}")


def create_comments():
    """Create comments"""
    url = (
        f"http://{config_info.HOST}:{config_info.API_PORT}"
        f"/{config_info.API_ROUTES[config_info.APIOperations.COMMENTS_CREATE]}"
    )
    for request in CREATE_COMMENT_REQUESTS:
        response = requests.post(
            url=url,
            json=request.dict()
        )
        print(f"[{response.json()['result']}] Create Comment Response for"
              f" request {request}: {response.json()}")


if __name__ == "__main__":
    create_users()
    create_projects()
    create_tasks()
    create_comments()
