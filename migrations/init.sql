DROP TABLE IF EXISTS public.shops;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.categories;
DROP TABLE IF EXISTS public.products;
DROP TABLE IF EXISTS public.paychecks;
DROP TABLE IF EXISTS public.shopping_carts;

CREATE TABLE public.shops (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    login VARCHAR(30) NOT NULL,
    password VARCHAR(30) NOT NULL
);

CREATE TABLE public.users (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    login VARCHAR (30) NOT NULL,
    password VARCHAR(30) NOT NULL
);

CREATE TABLE public.categories (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE public.products (
    id SERIAL PRIMARY KEY NOT NULL,
    category_id INT REFERENCES public.categories(id) ON DELETE SET NULL,
    name VARCHAR(50) NOT NULL,
    price MONEY NOT NULL,
    description TEXT
);

CREATE TABLE public.paychecks (
    id SERIAL PRIMARY KEY NOT NULL,
    paycheck_id INT NOT NULL,
    user_id INT REFERENCES public.users(id) ON DELETE SET NULL,
    product_id INT REFERENCES public.products(id) ON DELETE SET NULL
);

CREATE TABLE public.shopping_carts (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id INT REFERENCES public.users(id) ON DELETE SET NULL,
    product_id INT REFERENCES public.products(id) ON DELETE SET NULL
);