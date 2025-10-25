import csv
from io import StringIO
from collections import defaultdict

# ==============================================================================
# 1. Contenido de los Archivos (Definiciones de Datos)
#    Nota: En un entorno de consola, estos datos se leerían desde archivos
#    reales, pero para un script autocontenido, los pegamos aquí.
# ==============================================================================

# **ATENCIÓN:** Se asume que estos son los contenidos completos de tus archivos CSV.

CLIENTES_CSV_CONTENT = """id_cliente,nombre_cliente,email,ciudad,fecha_alta
1,Mariana Lopez,mariana.lopez@mail.com,Carlos Paz,2023-01-01
2,Nicolas Rojas,nicolas.rojas@mail.com,Carlos Paz,2023-01-02
3,Hernan Martinez,hernan.martinez@mail.com,Rio Cuarto,2023-01-03
4,Uma Martinez,uma.martinez@mail.com,Carlos Paz,2023-01-04
5,Agustina Flores,agustina.flores@mail.com,Cordoba,2023-01-05
6,Uma Medina,uma.medina@mail.com,Villa Maria,2023-01-06
7,Emilia Castro,emilia.castro@mail.com,Rio Cuarto,2023-01-07
8,Bruno Castro,bruno.castro@mail.com,Carlos Paz,2023-01-08
9,Yamila Molina,yamila.molina@mail.com,Carlos Paz,2023-01-09
10,Karina Acosta,karina.acosta@mail.com,Cordoba,2023-01-10
11,Helena Sanchez,helena.sanchez@mail.com,Villa Maria,2023-01-11
12,Gael Gomez,gael.gomez@mail.com,Alta Gracia,2023-01-12
13,Ivana Sanchez,ivana.sanchez@mail.com,Carlos Paz,2023-01-13
14,Gael Martinez,gael.martinez@mail.com,Carlos Paz,2023-01-14
15,Tomas Ruiz,tomas.ruiz@mail.com,Cordoba,2023-01-15
16,Felipe Alvarez,felipe.alvarez@mail.com,Rio Cuarto,2023-01-16
17,Pablo Gomez,pablo.gomez@mail.com,Villa Maria,2023-01-17
18,Ivana Torres,ivana.torres@mail.com,Carlos Paz,2023-01-18
19,Uma Silva,uma.silva@mail.com,Mendiolaza,2023-01-19
20,Tomas Acosta,tomas.acosta@mail.com,Rio Cuarto,2023-01-20
21,Elena Rodriguez,elena.rodriguez@mail.com,Alta Gracia,2023-01-21
22,Franco Rodriguez,franco.rodriguez@mail.com,Alta Gracia,2023-01-22
23,Helena Fernandez,helena.fernandez@mail.com,Rio Cuarto,2023-01-23
24,Nicolas Silva,nicolas.silva@mail.com,Villa Maria,2023-01-24
25,Karina Castro,karina.castro@mail.com,Rio Cuarto,2023-01-25
26,Camila Sanchez,camila.sanchez@mail.com,Alta Gracia,2023-01-26
27,Tomas Castro,tomas.castro@mail.com,Rio Cuarto,2023-01-27
28,Rocio Silva,rocio.silva@mail.com,Cordoba,2023-01-28
29,Diego Fernandez,diego.fernandez@mail.com,Alta Gracia,2023-01-29
30,Ivana Medina,ivana.medina@mail.com,Alta Gracia,2023-01-30
31,Felipe Ruiz,felipe.ruiz@mail.com,Villa Maria,2023-01-31
32,Martina Alvarez,martina.alvarez@mail.com,Mendiolaza,2023-02-01
33,Franco Acosta,franco.acosta@mail.com,Rio Cuarto,2023-02-02
34,Bruno Castro,bruno.castro2@mail.com,Villa Maria,2023-02-03
35,Yamila Lopez,yamila.lopez@mail.com,Mendiolaza,2023-02-04
36,Martina Molina,martina.molina@mail.com,Mendiolaza,2023-02-05
37,Martina Perez,martina.perez@mail.com,Mendiolaza,2023-02-06
38,Franco Herrera,franco.herrera@mail.com,Alta Gracia,2023-02-07
39,Santiago Diaz,santiago.diaz@mail.com,Alta Gracia,2023-02-08
40,Felipe Diaz,felipe.diaz@mail.com,Rio Cuarto,2023-02-09
41,Elena Rodriguez,elena.rodriguez2@mail.com,Alta Gracia,2023-02-10
42,Tomas Flores,tomas.flores@mail.com,Alta Gracia,2023-02-11
43,Lucas Perez,lucas.perez@mail.com,Mendiolaza,2023-02-12
44,Camila Romero,camila.romero@mail.com,Carlos Paz,2023-02-13
45,Olivia Castro,olivia.castro@mail.com,Rio Cuarto,2023-02-14
46,Agustina Martinez,agustina.martinez@mail.com,Alta Gracia,2023-02-15
47,Franco Silva,franco.silva@mail.com,Alta Gracia,2023-02-16
48,Rocio Alvarez,rocio.alvarez@mail.com,Cordoba,2023-02-17
49,Olivia Gomez,olivia.gomez@mail.com,Rio Cuarto,2023-02-18
50,Lucas Diaz,lucas.diaz@mail.com,Carlos Paz,2023-02-19
51,Agustina Gomez,agustina.gomez@mail.com,Rio Cuarto,2023-02-20
52,Diego Diaz,diego.diaz@mail.com,Rio Cuarto,2023-02-21
53,Emilia Rojas,emilia.rojas@mail.com,Mendiolaza,2023-02-22
54,Uma Herrera,uma.herrera@mail.com,Alta Gracia,2023-02-23
55,Olivia Ruiz,olivia.ruiz@mail.com,Mendiolaza,2023-02-24
56,Bruno Diaz,bruno.diaz@mail.com,Rio Cuarto,2023-02-25
57,Julian Acosta,julian.acosta@mail.com,Rio Cuarto,2023-02-26
58,Karina Acosta,karina.acosta2@mail.com,Rio Cuarto,2023-02-27
59,Emilia Ruiz,emilia.ruiz@mail.com,Villa Maria,2023-02-28
60,Uma Gonzalez,uma.gonzalez@mail.com,Alta Gracia,2023-03-01
61,Guadalupe Martinez,guadalupe.martinez@mail.com,Rio Cuarto,2023-03-02
62,Guadalupe Romero,guadalupe.romero@mail.com,Carlos Paz,2023-03-03
63,Pablo Medina,pablo.medina@mail.com,Cordoba,2023-03-04
64,Julian Alvarez,julian.alvarez@mail.com,Villa Maria,2023-03-05
65,Tomas Perez,tomas.perez@mail.com,Alta Gracia,2023-03-06
66,Tomas Herrera,tomas.herrera@mail.com,Villa Maria,2023-03-07
67,Ivana Romero,ivana.romero@mail.com,Alta Gracia,2023-03-08
68,Uma Torres,uma.torres@mail.com,Villa Maria,2023-03-09
69,Felipe Flores,felipe.flores@mail.com,Rio Cuarto,2023-03-10
70,Julian Diaz,julian.diaz@mail.com,Carlos Paz,2023-03-11
71,Valentina Alvarez,valentina.alvarez@mail.com,Villa Maria,2023-03-12
72,Camila Rodriguez,camila.rodriguez@mail.com,Cordoba,2023-03-13
73,Yamila Diaz,yamila.diaz@mail.com,Alta Gracia,2023-03-14
74,Zoe Flores,zoe.flores@mail.com,Carlos Paz,2023-03-15
75,Santiago Castro,santiago.castro@mail.com,Rio Cuarto,2023-03-16
76,Pablo Perez,pablo.perez@mail.com,Mendiolaza,2023-03-17
77,Bruno Alvarez,bruno.alvarez@mail.com,Villa Maria,2023-03-18
78,Emilia Alvarez,emilia.alvarez@mail.com,Villa Maria,2023-03-19
79,Olivia Perez,olivia.perez@mail.com,Carlos Paz,2023-03-20
80,Gael Ruiz,gael.ruiz@mail.com,Mendiolaza,2023-03-21
81,Camila Ruiz,camila.ruiz@mail.com,Carlos Paz,2023-03-22
82,Lucas Lopez,lucas.lopez@mail.com,Alta Gracia,2023-03-23
83,Franco Gomez,franco.gomez@mail.com,Rio Cuarto,2023-03-24
84,Pablo Sanchez,pablo.sanchez@mail.com,Cordoba,2023-03-25
85,Agustina Martinez,agustina.martinez2@mail.com,Mendiolaza,2023-03-26
86,Diego Torres,diego.torres@mail.com,Cordoba,2023-03-27
87,Bautista Lopez,bautista.lopez@mail.com,Alta Gracia,2023-03-28
88,Felipe Castro,felipe.castro@mail.com,Villa Maria,2023-03-29
89,Karina Martinez,karina.martinez@mail.com,Rio Cuarto,2023-03-30
90,Guadalupe Ruiz,guadalupe.ruiz@mail.com,Rio Cuarto,2023-03-31
91,Uma Sanchez,uma.sanchez@mail.com,Mendiolaza,2023-04-01
92,Mariana Rodriguez,mariana.rodriguez@mail.com,Alta Gracia,2023-04-02
93,Gael Rojas,gael.rojas@mail.com,Alta Gracia,2023-04-03
94,Elena Sanchez,elena.sanchez@mail.com,Mendiolaza,2023-04-04
95,Olivia Perez,olivia.perez2@mail.com,Rio Cuarto,2023-04-05
96,Rocio Gonzalez,rocio.gonzalez@mail.com,Cordoba,2023-04-06
97,Uma Alvarez,uma.alvarez@mail.com,Cordoba,2023-04-07
98,Camila Castro,camila.castro@mail.com,Cordoba,2023-04-08
99,Bruno Molina,bruno.molina@mail.com,Villa Maria,2023-04-09
100,Agustina Lopez,agustina.lopez@mail.com,Cordoba,2023-04-10
"""

PRODUCTOS_CSV_CONTENT = """id_producto,nombre_producto,categoria,precio_unitario
1,Coca Cola 1.5L,Alimentos,2347
2,Pepsi 1.5L,Limpieza,4973
3,Sprite 1.5L,Alimentos,4964
4,Fanta Naranja 1.5L,Limpieza,2033
5,Agua Mineral 500ml,Alimentos,4777
6,Jugo de Naranja 1L,Limpieza,4170
7,Jugo de Manzana 1L,Alimentos,3269
8,Energética Nitro 500ml,Limpieza,4218
9,Yerba Mate Suave 1kg,Alimentos,3878
10,Yerba Mate Intensa 1kg,Limpieza,4883
11,Café Molido 250g,Alimentos,2053
12,Té Negro 20 saquitos,Limpieza,570
13,Té Verde 20 saquitos,Alimentos,2383
14,Leche Entera 1L,Limpieza,1723
15,Leche Descremada 1L,Alimentos,2538
16,Yogur Natural 200g,Limpieza,4613
17,Queso Cremoso 500g,Alimentos,4834
18,Queso Rallado 150g,Limpieza,3444
19,Manteca 200g,Alimentos,3251
20,Pan Lactal Blanco,Limpieza,1571
21,Pan Lactal Integral,Alimentos,272
22,Medialunas de Manteca,Limpieza,2069
23,Bizcochos Salados,Alimentos,2380
24,Galletitas Chocolate,Limpieza,1305
25,Galletitas Vainilla,Alimentos,4015
26,Alfajor Triple,Limpieza,1001
27,Alfajor Simple,Alimentos,2502
28,Papas Fritas Clásicas 100g,Limpieza,936
29,Papas Fritas Onduladas 100g,Alimentos,1868
30,Maní Salado 200g,Limpieza,4875
31,Mix de Frutos Secos 200g,Alimentos,3409
32,Chocolate Amargo 100g,Limpieza,2234
33,Chocolate con Leche 100g,Alimentos,1255
34,Turrón 50g,Limpieza,503
35,Barrita de Cereal 30g,Alimentos,4430
36,Dulce de Leche 400g,Limpieza,2559
37,Mermelada de Durazno 400g,Alimentos,3196
38,Mermelada de Frutilla 400g,Limpieza,1584
39,Helado Vainilla 1L,Alimentos,469
40,Helado Chocolate 1L,Limpieza,1215
41,Aceite de Girasol 1L,Alimentos,860
42,Vinagre de Alcohol 500ml,Limpieza,1195
43,Salsa de Tomate 500g,Alimentos,887
44,Arroz Largo Fino 1kg,Limpieza,2979
45,Fideos Spaghetti 500g,Alimentos,745
46,Lentejas Secas 500g,Limpieza,3036
47,Garbanzos 500g,Alimentos,2939
48,Porotos Negros 500g,Limpieza,4462
49,Harina de Trigo 1kg,Alimentos,2512
50,Azúcar 1kg,Limpieza,727
51,Sal Fina 500g,Alimentos,1745
52,Detergente Líquido 750ml,Limpieza,2582
53,Lavandina 1L,Alimentos,1664
54,Jabón de Tocador,Limpieza,1592
55,Shampoo 400ml,Alimentos,1407
56,Papel Higiénico x4,Limpieza,2532
57,Servilletas x100,Alimentos,4520
58,Caramelos Masticables,Limpieza,4752
59,Chicle Menta,Alimentos,3612
60,Chupetín,Limpieza,4647
61,Miel Pura 250g,Alimentos,4982
62,Stevia 100 sobres,Limpieza,3848
63,Granola 250g,Alimentos,4337
64,Avena Instantánea 250g,Limpieza,3953
65,Cerveza Rubia 1L,Alimentos,2423
66,Cerveza Negra 1L,Limpieza,1533
67,Vino Tinto Malbec 750ml,Alimentos,4719
68,Vino Blanco 750ml,Limpieza,2684
69,Sidra 750ml,Alimentos,744
70,Fernet 750ml,Limpieza,4061
71,Vodka 700ml,Alimentos,508
72,Ron 700ml,Limpieza,3876
73,Gin 700ml,Alimentos,1561
74,Whisky 750ml,Limpieza,2953
75,Licor de Café 700ml,Alimentos,3204
76,Pizza Congelada Muzzarella,Limpieza,4286
77,Empanadas Congeladas,Alimentos,4778
78,Verduras Congeladas Mix,Limpieza,4289
79,Hamburguesas Congeladas x4,Alimentos,2420
80,Helado de Frutilla 1L,Limpieza,1981
81,Aceitunas Verdes 200g,Alimentos,2520
82,Aceitunas Negras 200g,Limpieza,2394
83,Queso Untable 190g,Alimentos,1830
84,Queso Azul 150g,Limpieza,1645
85,Jugo en Polvo Naranja,Alimentos,1856
86,Jugo en Polvo Limón,Limpieza,4090
87,Sopa Instantánea Pollo,Alimentos,1679
88,Caldo Concentrado Carne,Limpieza,2570
89,Caldo Concentrado Verdura,Alimentos,1003
90,Toallas Húmedas x50,Limpieza,2902
91,Desodorante Aerosol,Alimentos,4690
92,Crema Dental 90g,Limpieza,2512
93,Cepillo de Dientes,Alimentos,2142
94,Hilo Dental,Limpieza,1418
95,Mascarilla Capilar,Alimentos,1581
96,Suavizante 1L,Limpieza,4920
97,Limpiavidrios 500ml,Alimentos,872
98,Desengrasante 500ml,Limpieza,2843
99,Esponjas x3,Alimentos,2430
100,Trapo de Piso,Limpieza,4854
"""

VENTAS_CSV_CONTENT = """id_venta,fecha,id_cliente,nombre_cliente,email,medio_pago
1,2024-06-19,62,Guadalupe Romero,guadalupe.romero@mail.com,tarjeta
2,2024-03-17,49,Olivia Gomez,olivia.gomez@mail.com,qr
3,2024-01-13,20,Tomas Acosta,tomas.acosta@mail.com,tarjeta
4,2024-02-27,36,Martina Molina,martina.molina@mail.com,transferencia
5,2024-06-11,56,Bruno Diaz,bruno.diaz@mail.com,tarjeta
6,2024-05-05,91,Uma Sanchez,uma.sanchez@mail.com,transferencia
7,2024-05-06,92,Mariana Rodriguez,mariana.rodriguez@mail.com,efectivo
8,2024-01-06,66,Tomas Herrera,tomas.herrera@mail.com,transferencia
9,2024-01-20,86,Diego Torres,diego.torres@mail.com,efectivo
10,2024-05-28,52,Diego Diaz,diego.diaz@mail.com,qr
11,2024-04-10,20,Tomas Acosta,tomas.acosta@mail.com,qr
12,2024-06-28,96,Rocio Gonzalez,rocio.gonzalez@mail.com,efectivo
13,2024-01-24,6,Uma Medina,uma.medina@mail.com,tarjeta
14,2024-04-18,67,Ivana Romero,ivana.romero@mail.com,qr
15,2024-06-27,56,Bruno Diaz,bruno.diaz@mail.com,transferencia
16,2024-04-12,2,Nicolas Rojas,nicolas.rojas@mail.com,efectivo
17,2024-02-17,88,Felipe Castro,felipe.castro@mail.com,efectivo
18,2024-06-11,81,Camila Ruiz,camila.ruiz@mail.com,qr
19,2024-06-11,80,Gael Ruiz,gael.ruiz@mail.com,efectivo
20,2024-01-13,75,Santiago Castro,santiago.castro@mail.com,tarjeta
21,2024-06-19,10,Karina Acosta,karina.acosta@mail.com,transferencia
22,2024-05-08,64,Julian Alvarez,julian.alvarez@mail.com,transferencia
23,2024-05-16,78,Emilia Alvarez,emilia.alvarez@mail.com,transferencia
24,2024-06-14,55,Olivia Ruiz,olivia.ruiz@mail.com,tarjeta
25,2024-04-30,13,Ivana Sanchez,ivana.sanchez@mail.com,transferencia
26,2024-01-23,49,Olivia Gomez,olivia.gomez@mail.com,efectivo
27,2024-02-25,9,Yamila Molina,yamila.molina@mail.com,transferencia
28,2024-05-20,52,Diego Diaz,diego.diaz@mail.com,qr
29,2024-02-20,49,Olivia Gomez,olivia.gomez@mail.com,qr
30,2024-03-03,93,Gael Rojas,gael.rojas@mail.com,efectivo
31,2024-05-22,19,Uma Silva,uma.silva@mail.com,tarjeta
32,2024-01-30,31,Felipe Ruiz,felipe.ruiz@mail.com,efectivo
33,2024-02-13,6,Uma Medina,uma.medina@mail.com,efectivo
34,2024-01-13,58,Karina Acosta,karina.acosta2@mail.com,transferencia
35,2024-05-30,61,Guadalupe Martinez,guadalupe.martinez@mail.com,efectivo
36,2024-06-25,5,Agustina Flores,agustina.flores@mail.com,tarjeta
37,2024-05-17,57,Julian Acosta,julian.acosta@mail.com,qr
38,2024-05-29,56,Bruno Diaz,bruno.diaz@mail.com,tarjeta
39,2024-03-05,5,Agustina Flores,agustina.flores@mail.com,efectivo
40,2024-05-13,15,Tomas Ruiz,tomas.ruiz@mail.com,efectivo
41,2024-03-08,29,Diego Fernandez,diego.fernandez@mail.com,tarjeta
42,2024-04-18,12,Gael Gomez,gael.gomez@mail.com,tarjeta
43,2024-02-18,23,Helena Fernandez,helena.fernandez@mail.com,efectivo
44,2024-02-21,21,Elena Rodriguez,elena.rodriguez@mail.com,efectivo
45,2024-01-19,15,Tomas Ruiz,tomas.ruiz@mail.com,efectivo
46,2024-03-25,46,Agustina Martinez,agustina.martinez@mail.com,tarjeta
47,2024-05-04,52,Diego Diaz,diego.diaz@mail.com,transferencia
48,2024-01-26,84,Pablo Sanchez,pablo.sanchez@mail.com,qr
49,2024-06-02,5,Agustina Flores,agustina.flores@mail.com,efectivo
50,2024-01-09,8,Bruno Castro,bruno.castro@mail.com,transferencia
51,2024-02-18,39,Santiago Diaz,santiago.diaz@mail.com,efectivo
52,2024-05-10,5,Agustina Flores,agustina.flores@mail.com,tarjeta
53,2024-01-25,56,Bruno Diaz,bruno.diaz@mail.com,tarjeta
54,2024-03-26,1,Mariana Lopez,mariana.lopez@mail.com,tarjeta
55,2024-01-04,100,Agustina Lopez,agustina.lopez@mail.com,qr
56,2024-06-14,15,Tomas Ruiz,tomas.ruiz@mail.com,qr
57,2024-01-10,34,Bruno Castro,bruno.castro2@mail.com,efectivo
58,2024-02-04,48,Rocio Alvarez,rocio.alvarez@mail.com,transferencia
59,2024-04-28,62,Guadalupe Romero,guadalupe.romero@mail.com,tarjeta
60,2024-04-04,81,Camila Ruiz,camila.ruiz@mail.com,transferencia
61,2024-06-01,27,Tomas Castro,tomas.castro@mail.com,efectivo
62,2024-05-01,100,Agustina Lopez,agustina.lopez@mail.com,transferencia
63,2024-06-19,25,Karina Castro,karina.castro@mail.com,tarjeta
64,2024-03-07,58,Karina Acosta,karina.acosta2@mail.com,qr
65,2024-04-30,30,Ivana Medina,ivana.medina@mail.com,qr
66,2024-03-14,69,Felipe Flores,felipe.flores@mail.com,qr
67,2024-03-21,66,Tomas Herrera,tomas.herrera@mail.com,efectivo
68,2024-06-28,27,Tomas Castro,tomas.castro@mail.com,qr
69,2024-01-06,42,Tomas Flores,tomas.flores@mail.com,qr
70,2024-02-02,41,Elena Rodriguez,elena.rodriguez2@mail.com,transferencia
71,2024-06-02,40,Felipe Diaz,felipe.diaz@mail.com,qr
72,2024-02-17,26,Camila Sanchez,camila.sanchez@mail.com,qr
73,2024-05-16,42,Tomas Flores,tomas.flores@mail.com,transferencia
74,2024-04-26,56,Bruno Diaz,bruno.diaz@mail.com,efectivo
75,2024-05-23,61,Guadalupe Martinez,guadalupe.martinez@mail.com,qr
76,2024-05-15,75,Santiago Castro,santiago.castro@mail.com,tarjeta
77,2024-05-26,55,Olivia Ruiz,olivia.ruiz@mail.com,tarjeta
78,2024-04-29,12,Gael Gomez,gael.gomez@mail.com,qr
79,2024-06-06,57,Julian Acosta,julian.acosta@mail.com,qr
80,2024-03-25,54,Uma Herrera,uma.herrera@mail.com,efectivo
81,2024-03-09,49,Olivia Gomez,olivia.gomez@mail.com,transferencia
82,2024-01-25,19,Uma Silva,uma.silva@mail.com,tarjeta
83,2024-05-28,91,Uma Sanchez,uma.sanchez@mail.com,efectivo
84,2024-01-02,72,Camila Rodriguez,camila.rodriguez@mail.com,efectivo
85,2024-01-23,42,Tomas Flores,tomas.flores@mail.com,transferencia
86,2024-01-10,40,Felipe Diaz,felipe.diaz@mail.com,efectivo
87,2024-04-20,100,Agustina Lopez,agustina.lopez@mail.com,qr
88,2024-06-21,37,Martina Perez,martina.perez@mail.com,efectivo
89,2024-01-18,17,Pablo Gomez,pablo.gomez@mail.com,tarjeta
90,2024-01-08,46,Agustina Martinez,agustina.martinez@mail.com,qr
91,2024-02-19,39,Santiago Diaz,santiago.diaz@mail.com,efectivo
92,2024-02-09,42,Tomas Flores,tomas.flores@mail.com,transferencia
93,2024-01-29,90,Guadalupe Ruiz,guadalupe.ruiz@mail.com,efectivo
94,2024-03-06,41,Elena Rodriguez,elena.rodriguez2@mail.com,qr
95,2024-02-25,26,Camila Sanchez,camila.sanchez@mail.com,qr
96,2024-02-23,83,Franco Gomez,franco.gomez@mail.com,tarjeta
97,2024-06-16,39,Santiago Diaz,santiago.diaz@mail.com,efectivo
98,2024-01-12,43,Lucas Perez,lucas.perez@mail.com,transferencia
99,2024-03-13,51,Agustina Gomez,agustina.gomez@mail.com,transferencia
100,2024-06-08,69,Felipe Flores,felipe.flores@mail.com,qr
101,2024-03-28,72,Camila Rodriguez,camila.rodriguez@mail.com,efectivo
102,2024-03-29,18,Ivana Torres,ivana.torres@mail.com,efectivo
103,2024-03-11,39,Santiago Diaz,santiago.diaz@mail.com,efectivo
104,2024-06-17,86,Diego Torres,diego.torres@mail.com,qr
105,2024-02-06,1,Mariana Lopez,mariana.lopez@mail.com,transferencia
106,2024-03-24,82,Lucas Lopez,lucas.lopez@mail.com,transferencia
107,2024-05-21,14,Gael Martinez,gael.martinez@mail.com,efectivo
108,2024-03-25,9,Yamila Molina,yamila.molina@mail.com,tarjeta
109,2024-06-04,64,Julian Alvarez,julian.alvarez@mail.com,transferencia
110,2024-05-19,92,Mariana Rodriguez,mariana.rodriguez@mail.com,efectivo
111,2024-02-12,48,Rocio Alvarez,rocio.alvarez@mail.com,efectivo
112,2024-01-19,28,Rocio Silva,rocio.silva@mail.com,tarjeta
113,2024-03-08,98,Camila Castro,camila.castro@mail.com,transferencia
114,2024-05-05,16,Felipe Alvarez,felipe.alvarez@mail.com,qr
115,2024-02-16,3,Hernan Martinez,hernan.martinez@mail.com,transferencia
116,2024-03-18,25,Karina Castro,karina.castro@mail.com,qr
117,2024-03-14,72,Camila Rodriguez,camila.rodriguez@mail.com,tarjeta
118,2024-02-09,84,Pablo Sanchez,pablo.sanchez@mail.com,efectivo
119,2024-02-07,51,Agustina Gomez,agustina.gomez@mail.com,qr
120,2024-04-21,72,Camila Rodriguez,camila.rodriguez@mail.com,tarjeta
"""

DETALLE_CSV_CONTENT = """id_venta,id_producto,nombre_producto,cantidad,precio_unitario,importe
1,90,Toallas Húmedas x50,1,2902,2902
2,82,Aceitunas Negras 200g,5,2394,11970
2,39,Helado Vainilla 1L,5,469,2345
2,70,Fernet 750ml,2,,8122
2,22,Medialunas de Manteca,1,2069,2069
2,79,Hamburguesas Congeladas x4,4,2420,9680
3,9,Yerba Mate Suave 1kg,2,3878,7756
3,2,Pepsi 1.5L,2,4973,9946
3,85,Jugo en Polvo Naranja,1,1856,1856
4,4,Fanta Naranja 1.5L,2,2033,4066
4,23,Bizcochos Salados,5,2380,11900
5,86,Jugo en Polvo Limón,4,4090,16360
6,25,Galletitas Vainilla,2,4015,8030
6,31,Mix de Frutos Secos 200g,3,3409,10227
6,83,Queso Untable 190g,1,1830,1830
6,59,Chicle Menta,4,3612,14448
7,63,Granola 250g,3,4337,13011
8,53,Lavandina 1L,5,1664,8320
8,18,Queso Rallado 150g,4,3444,13776
8,68,Vino Blanco 750ml,5,,13420
9,65,Cerveza Rubia 1L,4,2423,9692
10,36,Dulce de Leche 400g,2,2559,5118
10,100,Trapo de Piso,4,4854,19416
10,37,Mermelada de Durazno 400g,3,3196,9588
10,62,Stevia 100 sobres,1,3848,3848
11,13,Té Verde 20 saquitos,1,2383,2383
11,65,Cerveza Rubia 1L,2,2423,4846
11,28,Papas Fritas Clásicas 100g,1,936,936
12,72,Ron 700ml,2,3876,7752
12,50,Azúcar 1kg,2,727,1454
12,56,Papel Higiénico x4,3,2532,7596
12,87,Sopa Instantánea Pollo,3,1679,5037
12,38,Mermelada de Frutilla 400g,4,1584,6336
13,87,Sopa Instantánea Pollo,1,1679,1679
13,81,Aceitunas Verdes 200g,3,2520,7560
13,13,Té Verde 20 saquitos,1,2383,2383
14,36,Dulce de Leche 400g,4,2559,10236
14,72,Ron 700ml,5,3876,19380
14,38,Mermelada de Frutilla 400g,3,1584,4752
14,97,Limpiavidrios 500ml,1,872,872
15,37,Mermelada de Durazno 400g,3,3196,9588
16,35,Barrita de Cereal 30g,5,4430,22150
17,81,Aceitunas Verdes 200g,5,2520,12600
17,46,Lentejas Secas 500g,5,3036,15180
17,74,Whisky 750ml,3,2953,8859
18,33,Chocolate con Leche 100g,2,1255,2510
18,4,Fanta Naranja 1.5L,5,2033,10165
18,24,Galletitas Chocolate,2,1305,2610
18,15,Leche Descremada 1L,3,2538,7614
18,22,Medialunas de Manteca,5,2069,10345
19,38,Mermelada de Frutilla 400g,2,1584,3168
19,98,Desengrasante 500ml,3,2843,8529
19,63,Granola 250g,3,4337,13011
20,32,Chocolate Amargo 100g,3,2234,6702
21,76,Pizza Congelada Muzzarella,5,4286,21430
21,35,Barrita de Cereal 30g,1,4430,4430
22,9,Yerba Mate Suave 1kg,2,3878,7756
22,28,Papas Fritas Clásicas 100g,3,936,2808
22,24,Galletitas Chocolate,4,1305,5220
23,64,Avena Instantánea 250g,4,3953,15812
23,83,Queso Untable 190g,4,1830,7320
24,91,Desodorante Aerosol,2,4690,9380
24,40,Helado Chocolate 1L,5,1215,6075
25,55,Shampoo 400ml,1,1407,1407
25,95,Mascarilla Capilar,5,1581,7905
25,72,Ron 700ml,1,3876,3876
26,79,Hamburguesas Congeladas x4,2,2420,4840
26,86,Jugo en Polvo Limón,1,4090,4090
27,7,Jugo de Manzana 1L,4,3269,13076
27,78,Verduras Congeladas Mix,4,4289,17156
28,74,Whisky 750ml,1,2953,2953
28,91,Desodorante Aerosol,2,4690,9380
28,72,Ron 700ml,1,3876,3876
28,18,Queso Rallado 150g,2,3444,6888
28,27,Alfajor Simple,5,2502,12510
29,58,Caramelos Masticables,1,4752,4752
29,36,Dulce de Leche 400g,2,2559,5118
29,71,Vodka 700ml,4,508,2032
29,27,Alfajor Simple,2,2502,5004
29,66,Cerveza Negra 1L,1,1533,1533
30,49,Harina de Trigo 1kg,4,2512,10048
30,78,Verduras Congeladas Mix,3,4289,12867
30,82,Aceitunas Negras 200g,4,2394,9576
30,7,Jugo de Manzana 1L,1,3269,3269
31,92,Crema Dental 90g,4,2512,10048
31,90,Toallas Húmedas x50,3,2902,8706
31,84,Queso Azul 150g,5,1645,8225
32,72,Ron 700ml,5,3876,19380
32,53,Lavandina 1L,4,1664,6656
32,17,Queso Cremoso 500g,3,4834,14502
32,35,Barrita de Cereal 30g,3,4430,13290
33,47,Garbanzos 500g,2,2939,5878
33,76,Pizza Congelada Muzzarella,4,4286,17144
33,100,Trapo de Piso,1,4854,4854
33,91,Desodorante Aerosol,2,4690,9380
34,10,Yerba Mate Intensa 1kg,1,4883,4883
34,32,Chocolate Amargo 100g,5,2234,11170
35,93,Cepillo de Dientes,3,2142,6426
35,80,Helado de Frutilla 1L,2,1981,3962
35,88,Caldo Concentrado Carne,5,2570,12850
36,50,Azúcar 1kg,4,727,2908
36,48,Porotos Negros 500g,2,4462,8924
37,18,Queso Rallado 150g,3,3444,10332
38,62,Stevia 100 sobres,5,3848,19240
38,14,Leche Entera 1L,3,1723,5169
38,65,Cerveza Rubia 1L,5,2423,12115
38,5,Agua Mineral 500ml,3,4777,14331
39,44,Arroz Largo Fino 1kg,4,2979,11916
39,22,Medialunas de Manteca,2,2069,4138
39,58,Caramelos Masticables,4,4752,19008
39,81,Aceitunas Verdes 200g,4,2520,10080
40,44,Arroz Largo Fino 1kg,2,2979,5958
41,51,Sal Fina 500g,1,1745,1745
41,15,Leche Descremada 1L,1,2538,2538
42,47,Garbanzos 500g,3,2939,8817
42,29,Papas Fritas Onduladas 100g,1,1868,1868
42,73,Gin 700ml,3,1561,4683
43,1,Coca Cola 1.5L,5,2347,11735
43,49,Harina de Trigo 1kg,2,2512,5024
43,66,Cerveza Negra 1L,2,1533,3066
44,48,Porotos Negros 500g,1,4462,4462
44,47,Garbanzos 500g,2,2939,5878
44,100,Trapo de Piso,2,4854,9708
45,12,Té Negro 20 saquitos,2,570,1140
45,18,Queso Rallado 150g,2,3444,6888
45,87,Sopa Instantánea Pollo,4,1679,6716
45,98,Desengrasante 500ml,1,2843,2843
45,52,Detergente Líquido 750ml,2,2582,5164
46,21,Pan Lactal Integral,1,272,272
47,43,Salsa de Tomate 500g,5,887,4435
47,6,Jugo de Naranja 1L,3,4170,12510
48,70,Fernet 750ml,1,4061,4061
48,54,Jabón de Tocador,5,1592,7960
48,57,Servilletas x100,4,4520,18080
49,59,Chicle Menta,2,3612,7224
49,21,Pan Lactal Integral,4,272,1088
49,59,Chicle Menta,4,3612,14448
49,18,Queso Rallado 150g,3,3444,10332
49,85,Jugo en Polvo Naranja,3,1856,5568
50,10,Yerba Mate Intensa 1kg,2,4883,9766
50,34,Turrón 50g,5,503,2515
50,58,Caramelos Masticables,5,4752,23760
50,32,Chocolate Amargo 100g,3,2234,6702
50,91,Desodorante Aerosol,4,4690,18760
51,31,Mix de Frutos Secos 200g,1,3409,3409
52,83,Queso Untable 190g,2,1830,3660
52,9,Yerba Mate Suave 1kg,4,3878,15512
52,81,Aceitunas Verdes 200g,5,2520,12600
52,38,Mermelada de Frutilla 400g,3,1584,4752
53,28,Papas Fritas Clásicas 100g,1,936,936
54,65,Cerveza Rubia 1L,1,2423,2423
54,18,Queso Rallado 150g,2,3444,6888
54,91,Desodorante Aerosol,3,4690,14070
54,8,Energética Nitro 500ml,3,4218,12654
55,39,Helado Vainilla 1L,4,469,1876
56,18,Queso Rallado 150g,5,3444,17220
57,31,Mix de Frutos Secos 200g,3,3409,10227
57,41,Aceite de Girasol 1L,4,860,3440
57,9,Yerba Mate Suave 1kg,5,3878,19390
57,76,Pizza Congelada Muzzarella,3,4286,12858
57,98,Desengrasante 500ml,4,2843,11372
58,43,Salsa de Tomate 500g,2,887,1774
58,11,Café Molido 250g,1,2053,2053
59,31,Mix de Frutos Secos 200g,1,3409,3409
59,8,Energética Nitro 500ml,2,4218,8436
59,97,Limpiavidrios 500ml,5,872,4360
60,43,Salsa de Tomate 500g,1,887,887
60,98,Desengrasante 500ml,3,2843,8529
60,15,Leche Descremada 1L,1,2538,2538
60,21,Pan Lactal Integral,2,272,544
60,91,Desodorante Aerosol,4,4690,18760
61,9,Yerba Mate Suave 1kg,3,3878,11634
61,19,Manteca 200g,3,3251,9753
62,47,Garbanzos 500g,4,2939,11756
62,95,Mascarilla Capilar,3,1581,4743
63,8,Energética Nitro 500ml,5,4218,21090
63,2,Pepsi 1.5L,2,4973,9946
63,70,Fernet 750ml,3,4061,12183
63,45,Fideos Spaghetti 500g,4,745,2980
64,4,Fanta Naranja 1.5L,2,2033,4066
64,41,Aceite de Girasol 1L,2,860,1720
65,77,Empanadas Congeladas,4,4778,19112
65,22,Medialunas de Manteca,3,2069,6207
65,38,Mermelada de Frutilla 400g,5,1584,7920
65,36,Dulce de Leche 400g,4,2559,10236
66,16,Yogur Natural 200g,3,4613,13839
67,53,Lavandina 1L,1,1664,1664
67,8,Energética Nitro 500ml,2,4218,8436
68,94,Hilo Dental,4,1418,5672
69,76,Pizza Congelada Muzzarella,4,4286,17144
69,74,Whisky 750ml,3,2953,8859
70,66,Cerveza Negra 1L,3,1533,4599
70,89,Caldo Concentrado Verdura,4,1003,4012
70,38,Mermelada de Frutilla 400g,3,1584,4752
71,11,Café Molido 250g,3,2053,6159
71,79,Hamburguesas Congeladas x4,4,2420,9680
71,100,Trapo de Piso,4,4854,19416
71,92,Crema Dental 90g,1,2512,2512
72,94,Hilo Dental,3,1418,4254
72,41,Aceite de Girasol 1L,4,860,3440
72,51,Sal Fina 500g,2,1745,3490
73,28,Papas Fritas Clásicas 100g,1,936,936
73,24,Galletitas Chocolate,3,1305,3915
73,19,Manteca 200g,1,3251,3251
74,32,Chocolate Amargo 100g,3,2234,6702
74,14,Leche Entera 1L,2,1723,3446
74,55,Shampoo 400ml,2,1407,2814
75,3,Sprite 1.5L,4,4964,19856
75,2,Pepsi 1.5L,5,4973,24865
76,22,Medialunas de Manteca,4,2069,8276
76,23,Bizcochos Salados,4,2380,9520
76,24,Galletitas Chocolate,1,1305,1305
76,11,Café Molido 250g,2,2053,4106
77,53,Lavandina 1L,2,1664,3328
77,41,Aceite de Girasol 1L,1,860,860
77,34,Turrón 50g,5,503,2515
77,98,Desengrasante 500ml,2,2843,5686
77,39,Helado Vainilla 1L,2,469,938
78,37,Mermelada de Durazno 400g,3,3196,9588
78,79,Hamburguesas Congeladas x4,5,2420,12100
78,17,Queso Cremoso 500g,2,4834,9668
78,85,Jugo en Polvo Naranja,1,1856,1856
78,39,Helado Vainilla 1L,2,469,938
79,81,Aceitunas Verdes 200g,2,2520,5040
79,56,Papel Higiénico x4,2,2532,5064
80,39,Helado Vainilla 1L,5,469,2345
80,30,Maní Salado 200g,3,4875,14625
80,41,Aceite de Girasol 1L,5,860,4300
81,10,Yerba Mate Intensa 1kg,2,4883,9766
82,38,Mermelada de Frutilla 400g,1,1584,1584
82,28,Papas Fritas Clásicas 100g,2,936,1872
82,29,Papas Fritas Onduladas 100g,5,1868,9340
82,82,Aceitunas Negras 200g,2,2394,4788
83,5,Agua Mineral 500ml,2,4777,9554
83,26,Alfajor Triple,2,1001,2002
83,73,Gin 700ml,5,1561,7805
83,51,Sal Fina 500g,2,1745,3490
84,83,Queso Untable 190g,5,1830,9150
84,76,Pizza Congelada Muzzarella,4,4286,17144
85,32,Chocolate Amargo 100g,4,2234,8936
85,80,Helado de Frutilla 1L,2,1981,3962
86,66,Cerveza Negra 1L,2,1533,3066
86,1,Coca Cola 1.5L,4,2347,9388
86,13,Té Verde 20 saquitos,5,2383,11915
86,41,Aceite de Girasol 1L,3,860,2580
87,53,Lavandina 1L,2,1664,3328
87,86,Jugo en Polvo Limón,2,4090,8180
88,7,Jugo de Manzana 1L,5,3269,16345
88,53,Lavandina 1L,5,1664,8320
88,8,Energética Nitro 500ml,4,4218,16872
89,72,Ron 700ml,2,3876,7752
90,79,Hamburguesas Congeladas x4,4,2420,9680
90,6,Jugo de Naranja 1L,2,4170,8340
91,57,Servilletas x100,3,4520,13560
92,10,Yerba Mate Intensa 1kg,2,4883,9766
92,43,Salsa de Tomate 500g,4,887,3548
93,80,Helado de Frutilla 1L,4,1981,7924
93,66,Cerveza Negra 1L,3,1533,4599
93,91,Desodorante Aerosol,3,4690,14070
94,24,Galletitas Chocolate,1,1305,1305
94,86,Jugo en Polvo Limón,5,4090,20450
94,98,Desengrasante 500ml,2,2843,5686
95,72,Ron 700ml,5,3876,19380
95,12,Té Negro 20 saquitos,1,570,570
96,81,Aceitunas Verdes 200g,3,2520,7560
96,68,Vino Blanco 750ml,1,2684,2684
96,11,Café Molido 250g,2,2053,4106
96,50,Azúcar 1kg,3,727,2181
97,59,Chicle Menta,5,3612,18060
97,36,Dulce de Leche 400g,1,2559,2559
97,4,Fanta Naranja 1.5L,3,2033,6099
98,28,Papas Fritas Clásicas 100g,4,936,3744
98,61,Miel Pura 250g,1,4982,4982
98,29,Papas Fritas Onduladas 100g,1,1868,1868
98,83,Queso Untable 190g,3,1830,5490
99,40,Helado Chocolate 1L,5,1215,6075
100,13,Té Verde 20 saquitos,3,2383,7149
100,18,Queso Rallado 150g,4,3444,13776
100,58,Caramelos Masticables,2,4752,9504
100,57,Servilletas x100,1,4520,4520
100,9,Yerba Mate Suave 1kg,4,3878,15512
101,34,Turrón 50g,4,503,2012
102,78,Verduras Congeladas Mix,3,4289,12867
102,36,Dulce de Leche 400g,3,2559,7677
103,79,Hamburguesas Congeladas x4,5,2420,12100
103,43,Salsa de Tomate 500g,5,887,4435
103,34,Turrón 50g,1,503,503
103,70,Fernet 750ml,1,4061,4061
104,95,Mascarilla Capilar,2,1581,3162
104,68,Vino Blanco 750ml,3,2684,8052
104,68,Vino Blanco 750ml,5,2684,13420
105,13,Té Verde 20 saquitos,2,2383,4766
105,4,Fanta Naranja 1.5L,4,2033,8132
105,58,Caramelos Masticables,2,4752,9504
105,82,Aceitunas Negras 200g,4,2394,9576
105,43,Salsa de Tomate 500g,5,887,4435
106,88,Caldo Concentrado Carne,3,2570,7710
107,7,Jugo de Manzana 1L,4,3269,13076
107,11,Café Molido 250g,2,2053,4106
107,12,Té Negro 20 saquitos,4,570,2280
107,5,Agua Mineral 500ml,4,4777,19108
108,90,Toallas Húmedas x50,4,2902,11608
109,18,Queso Rallado 150g,1,3444,3444
109,74,Whisky 750ml,1,2953,2953
109,20,Pan Lactal Blanco,2,1571,3142
109,44,Arroz Largo Fino 1kg,5,2979,14895
110,6,Jugo de Naranja 1L,1,4170,4170
110,59,Chicle Menta,3,3612,10836
110,6,Jugo de Naranja 1L,5,4170,20850
111,97,Limpiavidrios 500ml,4,872,3488
111,93,Cepillo de Dientes,3,2142,6426
111,20,Pan Lactal Blanco,2,1571,3142
111,23,Bizcochos Salados,4,2380,9520
112,55,Shampoo 400ml,1,1407,1407
112,21,Pan Lactal Integral,4,272,1088
112,43,Salsa de Tomate 500g,5,887,4435
112,13,Té Verde 20 saquitos,2,2383,4766
112,59,Chicle Menta,1,3612,3612
113,53,Lavandina 1L,2,1664,3328
113,92,Crema Dental 90g,3,2512,7536
114,8,Energética Nitro 500ml,1,4218,4218
114,84,Queso Azul 150g,1,1645,1645
114,10,Yerba Mate Intensa 1kg,1,4883,4883
114,55,Shampoo 400ml,5,1407,7035
114,92,Crema Dental 90g,4,2512,10048
115,17,Queso Cremoso 500g,4,4834,19336
115,97,Limpiavidrios 500ml,5,872,4360
115,95,Mascarilla Capilar,4,1581,6324
115,84,Queso Azul 150g,2,1645,3290
116,65,Cerveza Rubia 1L,1,2423,2423
116,35,Barrita de Cereal 30g,2,4430,8860
116,42,Vinagre de Alcohol 500ml,4,1195,4780
116,54,Jabón de Tocador,5,1592,7960
116,90,Toallas Húmedas x50,4,2902,11608
117,67,Vino Tinto Malbec 750ml,4,4719,18876
117,61,Miel Pura 250g,2,4982,9964
118,68,Vino Blanco 750ml,5,2684,13420
118,68,Vino Blanco 750ml,3,2684,8052
118,70,Fernet 750ml,2,4061,8122
118,93,Cepillo de Dientes,3,2142,6426
118,50,Azúcar 1kg,2,727,1454
119,45,Fideos Spaghetti 500g,5,745,3725
120,20,Pan Lactal Blanco,5,1571,7855
"""

# ==============================================================================
# Funciones de Carga y Preprocesamiento
# ==============================================================================

def cargar_datos(csv_content):
    """Carga una cadena CSV en una lista de diccionarios."""
    f = StringIO(csv_content.strip())
    lector = csv.DictReader(f)
    return list(lector)

def preprocesar_datos():
    """Carga, limpia y consolida los datos para el análisis."""
    datos_clientes = cargar_datos(CLIENTES_CSV_CONTENT)
    datos_productos = cargar_datos(PRODUCTOS_CSV_CONTENT)
    datos_ventas = cargar_datos(VENTAS_CSV_CONTENT)
    datos_detalle = cargar_datos(DETALLE_CSV_CONTENT)

    # 1. Mapeo para 'JOIN'
    producto_map = {item['id_producto']: item for item in datos_productos}
    
    # 2. Creación de la Tabla Maestra (Detalle + Info Adicional)
    maestra = []
    
    for detalle in datos_detalle:
        # Conversión de tipos y limpieza
        try:
            cantidad = int(detalle['cantidad'])
            importe = float(detalle['importe'])
            
            # Manejo de precio_unitario faltante
            precio_unitario = detalle['precio_unitario']
            if not precio_unitario:
                precio_unitario = importe / cantidad
            else:
                precio_unitario = float(precio_unitario)

            detalle['importe'] = importe # Usamos el valor original para sumas
            
            # Obtener categoría
            id_producto = detalle['id_producto']
            categoria = producto_map.get(id_producto, {}).get('categoria', 'Desconocida')
            detalle['categoria'] = categoria
            
            maestra.append(detalle)
        except Exception:
            # Ignorar líneas con errores graves de formato/valores
            continue
            
    return maestra, datos_clientes, datos_ventas

# ==============================================================================
# Funciones de Análisis (Respuesta a Comandos)
# ==============================================================================

def analizar_ventas_totales(maestra):
    """Calcula y muestra las ventas totales."""
    total_ventas = sum(linea['importe'] for linea in maestra)
    print(f"\n📈 **VENTAS TOTALES:**")
    print(f"Monto total de ventas: ${total_ventas:,.2f}")

def analizar_ventas_por_categoria(maestra):
    """Calcula y muestra el total de ventas por categoría."""
    ventas_por_categoria = defaultdict(float)
    for linea in maestra:
        ventas_por_categoria[linea['categoria']] += linea['importe']
    
    print(f"\n📊 **VENTAS POR CATEGORÍA:**")
    # Ordenar de mayor a menor
    top_categorias = sorted(ventas_por_categoria.items(), key=lambda item: item[1], reverse=True)
    for categoria, monto in top_categorias:
        print(f"- {categoria}: ${monto:,.2f}")

def analizar_top_productos(maestra, top_n=5):
    """Calcula y muestra los N productos con mayores ingresos."""
    productos_ingresos = defaultdict(float)
    for linea in maestra:
        productos_ingresos[linea['nombre_producto']] += linea['importe']
        
    print(f"\n🥇 **TOP {top_n} PRODUCTOS POR INGRESO:**")
    top_productos = sorted(productos_ingresos.items(), key=lambda item: item[1], reverse=True)[:top_n]
    for producto, ingreso in top_productos:
        print(f"- {producto}: ${ingreso:,.2f}")

def analizar_medios_pago(datos_ventas):
    """Calcula y muestra la distribución de medios de pago por transacción."""
    conteo_medios_pago = defaultdict(int)
    for venta in datos_ventas:
        conteo_medios_pago[venta['medio_pago']] += 1
        
    total_transacciones = len(datos_ventas)
    print(f"\n💳 **DISTRIBUCIÓN DE MEDIOS DE PAGO ({total_transacciones} Transacciones):**")
    
    # Ordenar por el conteo (más usado primero)
    medios_ordenados = sorted(conteo_medios_pago.items(), key=lambda item: item[1], reverse=True)
    
    for medio, conteo in medios_ordenados:
        porcentaje = (conteo / total_transacciones) * 100
        print(f"- {medio.capitalize()}: {conteo} ({porcentaje:.2f}%)")

def analizar_clientes_ciudad(datos_clientes, top_n=3):
    """Calcula y muestra las N ciudades con más clientes."""
    conteo_ciudades = defaultdict(int)
    for cliente in datos_clientes:
        conteo_ciudades[cliente['ciudad']] += 1
        
    print(f"\n🏘️ **TOP {top_n} CIUDADES POR CLIENTES:**")
    top_ciudades = sorted(conteo_ciudades.items(), key=lambda item: item[1], reverse=True)[:top_n]
    for ciudad, conteo in top_ciudades:
        print(f"- {ciudad}: {conteo} clientes")

def mostrar_ayuda():
    """Muestra la lista de comandos disponibles."""
    print("\n--- COMANDOS DISPONIBLES ---")
    print("  **total** : Muestra las ventas totales.")
    print("  **categoria** : Muestra el total de ventas por categoría.")
    print("  **top [N]** : Muestra los N productos con más ingresos (ej: top 5).")
    print("  **pago** : Muestra la distribución de medios de pago.")
    print("  **ciudad** : Muestra las ciudades con más clientes.")
    print("  **ayuda** : Muestra esta lista de comandos.")
    print("  **salir** : Cierra el programa.")
    print("----------------------------")

# ==============================================================================
# Bucle Principal Interactivo
# ==============================================================================

def main():
    """Función principal que ejecuta el bucle interactivo."""
    # 1. Carga y preprocesamiento inicial
    maestra, datos_clientes, datos_ventas = preprocesar_datos()
    
    print("===============================================")
    print("🛒 BIENVENIDO al Análisis de Datos de la Tienda")
    print("===============================================")
    mostrar_ayuda()

    while True:
        comando_input = input("\nIngrese comando > ").strip().lower()
        partes = comando_input.split()
        comando = partes[0] if partes else ""

        if comando == 'salir':
            print("👋 Saliendo del programa. ¡Hasta luego!")
            break
        
        elif comando == 'ayuda':
            mostrar_ayuda()

        elif comando == 'total':
            analizar_ventas_totales(maestra)
        
        elif comando == 'categoria':
            analizar_ventas_por_categoria(maestra)

        elif comando == 'top':
            n = 5 # Valor por defecto
            if len(partes) > 1 and partes[1].isdigit():
                n = int(partes[1])
            analizar_top_productos(maestra, n)

        elif comando == 'pago':
            analizar_medios_pago(datos_ventas)
            
        elif comando == 'ciudad':
            n = 3 # Valor por defecto
            if len(partes) > 1 and partes[1].isdigit():
                n = int(partes[1])
            analizar_clientes_ciudad(datos_clientes, n)

        elif comando:
            print(f"❌ Comando '{comando}' no reconocido. Escriba 'ayuda' para ver las opciones.")

if __name__ == "__main__":
    main()