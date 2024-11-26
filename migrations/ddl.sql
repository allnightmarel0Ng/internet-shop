DROP TABLE IF EXISTS public.shops CASCADE;
DROP TABLE IF EXISTS public.users CASCADE;
DROP TABLE IF EXISTS public.categories CASCADE;
DROP TABLE IF EXISTS public.products CASCADE;
DROP TABLE IF EXISTS public.paychecks CASCADE;
DROP TABLE IF EXISTS public.shopping_carts CASCADE;

CREATE TABLE public.shops (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    login VARCHAR(30) NOT NULL UNIQUE,
    password_hash VARCHAR(70) NOT NULL
);

CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    login VARCHAR (30) NOT NULL UNIQUE,
    password_hash VARCHAR(70) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL CHECK (balance > 0)
);

CREATE TABLE public.categories (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE public.products (
    id SERIAL PRIMARY KEY NOT NULL,
    category_id INT REFERENCES public.categories(id) ON DELETE SET NULL,
    shop_id INT REFERENCES public.shops(id) ON DELETE SET NULL,
    name VARCHAR(50) NOT NULL,
    price MONEY NOT NULL,
    description TEXT
);

CREATE TABLE public.paychecks (
    id SERIAL PRIMARY KEY NOT NULL,
    paycheck_id INT NOT NULL,
    user_id INT REFERENCES public.users(id) ON DELETE SET NULL,
    product_id INT REFERENCES public.products(id) ON DELETE SET NULL,
    creation_datetime TIME NOT NULL DEFAULT NOW()
);

CREATE TABLE public.shopping_carts (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id INT REFERENCES public.users(id) ON DELETE SET NULL,
    product_id INT REFERENCES public.products(id) ON DELETE SET NULL
);