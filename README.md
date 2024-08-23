# OTP Authentication via Email

## Project Description

This project is a simple OTP (One-Time Password) authentication system using FastAPI. It allows users to create an account with their email and log in using an OTP sent to their email address. The email is unique for each account. If an email does not exist and a user tries to log in, the system automatically creates an account and sends the OTP via that email. OTPs are temporarily stored in Redis for 5 minutes.

## Features

- Create an account with an email address.
- Login using an OTP sent to the email.
- Automatic account creation if the email is not registered.
- OTPs temporarily stored in Redis for 5 minutes.
- Email-based OTP generation and validation.
- Returns a token upon successful login.

## Prerequisites

- Python 3.11+
- FastAPI
- Postgresql
- Redis

## Start application with Docker Compose
Setup [Environment Configuration](#environment-configuration)

1. **Build the image**

   ```bash
   docker build -t app/otp .
   docker-compose up
   ```

## Installation

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2. **Set up a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
4. **Set up Postgresql:**

    - Install postgresql on your system.

5. **Set up Redis:**
    - Install Redis on your system or use a Redis cloud service.

6. #### Environment Configuration

    Create a `.env` file in the root directory and configure the following variables:

    ```env
    POSTGRES_HOST=
    POSTGRES_PORT=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_DB=
    AUTH_SECRETE_KEY=
    AUTH_ALGORITHM=
    MAIL_USERNAME=
    MAIL_PASSWORD=
    MAIL_FROM_NAME=
    MAIL_FROM=
    MAIL_PORT=
    MAIL_SERVER=
    MAIL_STARTTLS=
    MAIL_SSL_TLS=
    MAIL_USE_CREDENTIALS=
    MAIL_VALIDATE_CERTS=
    REDIS_HOST=
    REDIS_PORT=
    ```
    Pydantic config validation
    ```pydantic
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    AUTH_SECRETE_KEY: str
    AUTH_ALGORITHM: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM_NAME: Optional[str] = None
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool | None = True
    MAIL_SSL_TLS: bool | None = False
    MAIL_USE_CREDENTIALS: bool | None = True
    MAIL_VALIDATE_CERTS: bool | None = True
    REDIS_HOST: str | None = 'redis'
    REDIS_PORT: int | None = 6379
   ```

## Running the Application

1. **Start the Postgresql and Redis server:**

    Ensure your both servers are running.

2. **Start the FastAPI server:**

    ```bash
    uvicorn main:app --reload
    ```

3. **Access the application:**

    The application will be available at `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.

## Endpoints

### User Endpoints

- **Create User**
  - **Endpoint:** `POST /api/users`
  - **Description:** Create a new user account.
  - **Request Body:** `UserSchemaIn` (email required)
  - **Response:** `UserSchemaOut`

- **Get All Users**
  - **Endpoint:** `GET /api/users`
  - **Description:** Retrieve all users.
  - **Response:** `List[UserSchemaOut]`

- **Get User by Email**
  - **Endpoint:** `GET /api/users/email`
  - **Description:** Retrieve a user by their email address.
  - **Query Parameter:** `email` (required)
  - **Response:** `UserSchemaOut`

### Authentication Endpoints

- **Generate OTP**
  - **Endpoint:** `POST /api/auth/otp/generates`
  - **Description:** Generate and send an OTP to the provided email address.
  - **Request Body:** `OtpGenerateSchemaIn` (email required)
  - **Response:** `OtpGenerateSchemaOut`

- **Login with OTP**
  - **Endpoint:** `POST /api/auth/otp/login`
  - **Description:** Log in using the provided email and OTP. Returns a token upon successful login.
  - **Request Body:** `OtpLoginSchemaIn` (email and OTP required)
  - **Response:** `OtpLoginSchemaOut` (includes token)

## Project Structure

```bash
.
├── app
│   ├── controllers
│   ├── models
│   ├── schemas
│   ├── services
│   ├── config
│   └── utils
├── main.py
├── requirements.txt
└── README.md
`
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact **Ernest Kwabena Asare** at [ernestasare2411@gmail.com](mailto:ernestasare2411@gmail.com).
