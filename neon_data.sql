--
-- PostgreSQL database dump
--

\restrict zZr9Kf9NCDlHETjWrzxO6i4kd2lr1dx5m6GtAaXQw1451TW4Woykb3Zt2W7mAjk

-- Dumped from database version 17.5 (6bc9ef8)
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: users_sync; Type: TABLE DATA; Schema: neon_auth; Owner: -
--

COPY neon_auth.users_sync (raw_json, updated_at, deleted_at) FROM stdin;
\.


--
-- Data for Name: accounts_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, role, team) FROM stdin;
7	pbkdf2_sha256$1000000$UJiIVI16v0xaln8kBFZK4r$qbzC0I64Ehzt7dGwn7ynDKnzlQyGkQ0VQGqmOhUetLQ=	2025-10-21 07:44:12.473886+00	t	Operations@Lp	Navya	Rajgopal	navyalifeplanner@gmail.com	t	t	2025-08-06 04:53:58+00	OPS	1
9	pbkdf2_sha256$1000000$a02cZoPFFhCkUkBnukQ3A4$4h17cTLa6KmPqq1msqijo9n3UuKwsfU9+tJz5Wm2bA4=	2025-08-23 08:34:45+00	f	lifeplannerktm_am	ardra	unnikrishnan	lifeplannerktm@gmail.com	t	t	2025-08-06 05:17:53+00	ADM_MANAGER	1
10	pbkdf2_sha256$1000000$VsGzLmMg2yn3QiHHLklrSj$uD8CQ4dvdBEgT+AYGNqszTej3Tuhx3KIb2aX9dbYNrI=	2025-09-19 05:29:17+00	f	stephie_roby	stephie	roby		t	t	2025-08-06 05:25:32+00	TRAINER	
6	pbkdf2_sha256$1000000$1Gn7HKVSR1CRQHWL7AE5Pa$B5ksjY7M0I/AkZI+iJ/9Q+EqLopbY01+EvaeBg2badc=	2025-08-16 04:38:21+00	f	suhaila_admissions	suhaila	T.V.	counsellorchn4@gmail.com	t	t	2025-08-06 04:20:21+00	ADM_MANAGER	1
12	pbkdf2_sha256$1000000$Fof6TXCDU62270OF7mdOM3$TTxJHRz++QiS6xKSUqiLoz17U3Yg41mU47DqLvWsn7M=	2025-10-22 04:51:46.704313+00	f	jyothi_lifeplanner	jyothi	K.S	lifeplannercochin@gmail.com	t	t	2025-09-30 11:07:13+00	ADM_MANAGER	1
13	pbkdf2_sha256$1000000$JChfVvYBoX7M4bPc74MRgr$WrZPAFcHNCxj3WgGVde8KA1e+SF6ho9YvEPaL/lZVl8=	2025-10-22 09:02:43.598438+00	t	govind_hob	govind	venugopal	hob@lifeplanneruniversal.com	t	t	2025-10-04 06:33:16+00	BUSINESS_HEAD	1
2	pbkdf2_sha256$1000000$HbHIlni8FaYktOYJ3B9HUY$zc1fYueREw2gp2yckhkf0eXjSoShMqd96XWLJIuOXY4=	2025-10-23 03:55:06.030283+00	f	lp_media	lifeplanner	media	lifeplannermedia@gmail.com	t	t	2025-08-05 11:25:05+00	MEDIA	1
5	pbkdf2_sha256$1000000$wEQHY022InlvL3JJDkKnS8$1IQtwdpFvsAiZb8qZucICG1j1Tib21jmTHOKQ/G+zUM=	2025-10-23 04:40:06.07642+00	f	aleena_admissions	aleena	shaji	counsellorchn2@gmail.com	t	t	2025-08-06 04:15:39+00	ADM_MANAGER	1
4	pbkdf2_sha256$1000000$LpK86eXo4Jqd8fPiwmqv2n$fFgr/EUoSzAauBPngoIJjYtexzM7HTOvs9i8jZusUDU=	2025-10-21 06:31:34.708962+00	f	aneeta_processing	aneeta	bernad	admissionslifeplanner@gmail.com	t	t	2025-08-06 04:13:20+00	PROCESSING	1
14	pbkdf2_sha256$1000000$NsgNbUWU2OJAyGYQGEArqQ$EmlB9HnnwSgChpLBy5a+4+j+iuxeRxYfIwVeXctYJfs=	2025-10-17 08:09:51.565329+00	f	ishi_elizabeth	ishi	elizabeth	flagchn6@gmail.com	f	t	2025-10-17 08:08:08+00	TRAINER	1
1	pbkdf2_sha256$1000000$cnFmYQEwweCeqPdNBj2XcT$m/UNqoZyX1RjB7ZH67DDJ1VsEXn9uen15bbjN5RxaEQ=	2025-10-14 10:41:13.919127+00	t	Admin@Lp			lifeplannermedia@gmail.com	t	t	2025-08-05 07:42:32+00	ADMIN	
8	pbkdf2_sha256$1000000$tKZpoq77hGljAGZtDbd8tC$ifm69hDL0f/+XkMg45ISHnLEPtEX0qlDcp1Q2ipVCUw=	2025-10-21 07:41:50.329827+00	f	aektm_lp	sreedevi	K.M.	counsellorktm2@gmail.com	t	t	2025-08-06 05:14:48+00	ADM_EXEC	1
11	pbkdf2_sha256$1000000$p5gDLG2Z7LlNx7lBUN5ygD$a87KADPG/2SNFRRncVqtEaJiI7X94iadmBBtWOCL8nU=	2025-08-20 07:21:21+00	f	bintu_admissions	bintu	mariyam	lifeplannerktm2@gmail.com	t	t	2025-08-08 05:04:30+00	ADM_MANAGER	1
\.


--
-- Data for Name: accounts_dailyreport; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts_dailyreport (id, report_text, created_at, updated_at, report_date, user_id, heading, name) FROM stdin;
6	Shot university delegates. Edited lp binta testimonial	2025-10-14 10:36:30.123148+00	2025-10-14 10:36:30.123166+00	2025-10-14	2	Work report	Priyan
7	Edit binta flag testimonial, Edit delegate anchor video.	2025-10-14 10:37:30.149471+00	2025-10-14 10:37:30.149487+00	2025-10-14	2	Agenda	Priyan
8	crm updates \r\noptimised loading speed of lifeplanneruniversal.com,fdsadmin	2025-10-14 10:47:03.972606+00	2025-10-14 10:47:03.972622+00	2025-10-14	2	Report	Risheb
9	crm updates,voxbay inegration	2025-10-14 10:53:50.024228+00	2025-10-14 10:53:50.024242+00	2025-10-14	2	Agenda	Risheb
10	FDS promotion\r\nSocial media posting\r\n\r\nAgenda\r\nSocial media posting\r\nbacklink building	2025-10-15 04:15:37.110166+00	2025-10-15 04:15:37.110182+00	2025-10-14	2	Work Report	Work Report
11	Backlink Bulding\r\nsocial media analysing	2025-10-15 12:14:21.857689+00	2025-10-15 12:14:21.857705+00	2025-10-15	2	Work Report	Anurag
12	Backlink Bulding\r\nsocial media analysing	2025-10-15 12:14:22.222425+00	2025-10-15 12:14:22.22244+00	2025-10-15	2	Work Report	Anurag
13	backlink building\r\nsocial media posting	2025-10-15 12:15:20.475124+00	2025-10-15 12:15:20.475138+00	2025-10-15	2	agenda	Anurag
14	uea dlegate anchor video. Hosted demo session for whattsap automation for bash.	2025-10-16 03:54:19.861204+00	2025-10-16 03:54:19.86122+00	2025-10-16	2	Work report	Priyan
15	delegate highlight, binta flag	2025-10-16 03:55:04.409863+00	2025-10-16 03:55:04.409877+00	2025-10-16	2	agenda	Priyan
17	backlink building\r\nsocial media posting	2025-10-16 12:25:46.343864+00	2025-10-16 12:25:46.34388+00	2025-10-16	2	Work report	Anurag
18	Backlink building\r\nsocial media posting	2025-10-16 12:26:12.874041+00	2025-10-16 12:26:12.874058+00	2025-10-16	2	Agenda	Anurag
19	report voxbay integration\r\nagendvoxbay integration 	2025-10-16 17:13:56.485642+00	2025-10-16 17:13:56.485657+00	2025-10-16	2	report and agenda	Risheb
20	report two thumbnails\r\nagenda, more thumbnails	2025-10-17 03:23:16.579313+00	2025-10-17 03:23:16.57933+00	2025-10-17	2	report and agenda	matthew 
21	Finished one delegate explaining video, finished binta flag video\r\nagenda\r\ncorrect logo on delegate video,\r\nshoot testimonial, do two more delegate videos, review problem of unviewable video with pratyush.	2025-10-17 16:32:20.403946+00	2025-10-17 16:32:20.403962+00	2025-10-17	2	work report and agenda 17.10.25	Priyan
22	backlink building\r\nfds promotion\r\nagenda\r\nsocial media posting\r\nbacklink building	2025-10-17 16:35:26.493514+00	2025-10-17 16:35:26.493529+00	2025-10-17	2	17.10.25 report 	anurag
23	thumbnails and posters.\r\nagenda\r\nthumbnails and posters	2025-10-17 16:36:02.892123+00	2025-10-17 16:36:02.892139+00	2025-10-17	2	17.10.25 report and agenda	matthew
24	Report\r\nsocial media posting\r\nbacklink building\r\nschedule social media posting\r\nagenda\r\nbacklink building\r\nsocial media posting.	2025-10-18 09:14:36.937779+00	2025-10-18 09:14:36.937794+00	2025-10-18	2	Agenda and report 18.10.25	Anurag
25	Report\r\nausbildung 3 posters\r\nfds kerala manga 1 poster\r\nagenda\r\nfds kerala manga poster\r\nthumbnails	2025-10-18 09:15:58.509172+00	2025-10-18 09:15:58.509185+00	2025-10-18	2	Agenda and report 18.10.25	Mathhew
26	report\r\ncreated razorpay account\r\nintegreated payment gateway in flaggurukulam website\r\nagenda\r\nadding new fee structure 	2025-10-18 09:17:27.96979+00	2025-10-18 09:17:27.969804+00	2025-10-18	2	Agenda and report 18.10.25	risheb
27	Report\r\nfds dillu testimonial audio issue resolved\r\nshot cerine lp testimonial\r\nediting cerine testimonial\r\nedited opening shot of delegate video.\r\nAgenda\r\nfinish cerine testimonial\r\ntwo more delegate videos\r\n1 fds testimonial\r\n	2025-10-18 09:19:50.36683+00	2025-10-18 09:19:50.366844+00	2025-10-18	2	Agenda and report 18.10.25	Priyan
28	upadated flag fee structure integrated with new payment gateway	2025-10-20 15:18:36.83301+00	2025-10-20 15:18:36.833025+00	2025-10-20	2	Work Report	Risheb
29	works on trainers section	2025-10-20 15:19:45.946756+00	2025-10-20 15:19:45.946771+00	2025-10-20	2	agenda	Risheb.s
31	started trainers section	2025-10-21 11:23:53.933106+00	2025-10-21 11:23:53.933122+00	2025-10-21	2	Work Report	Risheb
32	Trainers section	2025-10-21 11:24:47.368369+00	2025-10-21 11:24:47.368385+00	2025-10-21	2	Agenda	Risheb
33	fds poster boosting\r\nsocial media analysing	2025-10-21 11:25:32.967548+00	2025-10-21 11:25:32.967565+00	2025-10-21	2	Report	Anurag
34	Social media posting\r\nbacklinking	2025-10-21 11:26:08.35308+00	2025-10-21 11:26:08.353096+00	2025-10-21	2	agenda	Anurag
35	Casting call Poster\r\nSeminar Poster	2025-10-21 11:28:25.019563+00	2025-10-21 11:28:25.019579+00	2025-10-21	2	Work Report	Mathews
36	Lulu leads : 28\r\nXavier sirs leads : 8\r\nManorama follow ups : 15	2025-10-21 11:32:48.066885+00	2025-10-21 11:32:48.066899+00	2025-10-21	12	Daily Report	Jyothi KS
38	report\r\nmary cerine lp testimonila\r\nlp seminar video with isha\r\nagenda\r\n2 flag videos	2025-10-23 04:18:35.416391+00	2025-10-23 04:18:35.416409+00	2025-10-23	2	Agenda and report 22.10.25	Priyan Prince
39	report\r\nmary cerine lp testimonila\r\nlp seminar video with isha\r\nagenda\r\n2 flag videos	2025-10-23 04:18:35.417198+00	2025-10-23 04:18:35.417211+00	2025-10-23	2	Agenda and report 22.10.25	Priyan Prince
40	report\r\nmary cerine lp testimonila\r\nlp seminar video with isha\r\nagenda\r\n2 flag videos	2025-10-23 04:18:36.090414+00	2025-10-23 04:18:36.090431+00	2025-10-23	2	Agenda and report 22.10.25	Priyan Prince
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: accounts_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	accounts	user
7	leads	lead
8	leads	processingupdate
9	trainers	trainer
10	trainers	student
11	leads	remarkhistory
12	tasks	task
13	tasks	taskupdate
14	hob	hobsetting
15	hob	dailyreport
16	accounts	dailyreport
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add user	6	add_user
22	Can change user	6	change_user
23	Can delete user	6	delete_user
24	Can view user	6	view_user
25	Can add Lead	7	add_lead
26	Can change Lead	7	change_lead
27	Can delete Lead	7	delete_lead
28	Can view Lead	7	view_lead
29	Can add processing update	8	add_processingupdate
30	Can change processing update	8	change_processingupdate
31	Can delete processing update	8	delete_processingupdate
32	Can view processing update	8	view_processingupdate
33	Can add trainer	9	add_trainer
34	Can change trainer	9	change_trainer
35	Can delete trainer	9	delete_trainer
36	Can view trainer	9	view_trainer
37	Can add student	10	add_student
38	Can change student	10	change_student
39	Can delete student	10	delete_student
40	Can view student	10	view_student
41	Can add remark history	11	add_remarkhistory
42	Can change remark history	11	change_remarkhistory
43	Can delete remark history	11	delete_remarkhistory
44	Can view remark history	11	view_remarkhistory
45	Can add task	12	add_task
46	Can change task	12	change_task
47	Can delete task	12	delete_task
48	Can view task	12	view_task
49	Can add task update	13	add_taskupdate
50	Can change task update	13	change_taskupdate
51	Can delete task update	13	delete_taskupdate
52	Can view task update	13	view_taskupdate
53	Can add hob setting	14	add_hobsetting
54	Can change hob setting	14	change_hobsetting
55	Can delete hob setting	14	delete_hobsetting
56	Can view hob setting	14	view_hobsetting
57	Can add daily report	15	add_dailyreport
58	Can change daily report	15	change_dailyreport
59	Can delete daily report	15	delete_dailyreport
60	Can view daily report	15	view_dailyreport
61	Can add Daily Report	16	add_dailyreport
62	Can change Daily Report	16	change_dailyreport
63	Can delete Daily Report	16	delete_dailyreport
64	Can view Daily Report	16	view_dailyreport
\.


--
-- Data for Name: accounts_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.accounts_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2025-08-05 11:25:09.579468+00	2	neethu_lifeplanner ()	1	[{"added": {}}]	6	1
2	2025-08-05 11:28:39.633793+00	2	neethu_lifeplanner (Media Team)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team", "Staff status", "Superuser status"]}}]	6	1
3	2025-08-05 11:39:48.280071+00	3	lifeplannerchn2 ()	1	[{"added": {}}]	6	2
4	2025-08-05 11:40:31.3297+00	3	lifeplannerchn2 (Admission Manager)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team", "Staff status", "Superuser status"]}}]	6	2
5	2025-08-05 11:40:35.351826+00	3	lifeplannerchn2 (Admission Manager)	2	[]	6	2
6	2025-08-06 04:13:20.944436+00	4	aneeta_processing ()	1	[{"added": {}}]	6	1
7	2025-08-06 04:14:46.784099+00	4	aneeta_processing (Processing Executive)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team", "Staff status", "Superuser status"]}}]	6	1
8	2025-08-06 04:15:40.260183+00	5	aleena_admissions ()	1	[{"added": {}}]	6	1
9	2025-08-06 04:16:26.513339+00	5	aleena_admissions (Admission Manager)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team", "Staff status", "Superuser status"]}}]	6	1
10	2025-08-06 04:19:39.099029+00	2	neethu_media (Media Team)	2	[{"changed": {"fields": ["Username"]}}]	6	1
11	2025-08-06 04:20:21.74532+00	6	suhaila_admissions ()	1	[{"added": {}}]	6	1
12	2025-08-06 04:21:30.958649+00	6	suhaila_admissions (Admission Manager)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team", "Staff status", "Superuser status"]}}]	6	1
13	2025-08-06 04:22:15.398036+00	3	lifeplannerchn2 (Admission Manager)	3		6	1
14	2025-08-06 04:40:01.22374+00	1	lpadmin ()	2	[{"changed": {"fields": ["password"]}}]	6	1
15	2025-08-06 04:40:58.775462+00	1	Admin@Lp (General Manager)	2	[{"changed": {"fields": ["Username", "Role"]}}]	6	1
16	2025-08-06 04:53:59.519366+00	7	Operations@Lp ()	1	[{"added": {}}]	6	1
17	2025-08-06 05:14:49.686799+00	8	sreedevi_ae ()	1	[{"added": {}}]	6	1
18	2025-08-06 05:15:52.479108+00	8	sreedevi_ae (Admission Executive)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team", "Staff status", "Superuser status"]}}]	6	1
19	2025-08-06 05:17:54.581916+00	9	lifeplannerktm_am ()	1	[{"added": {}}]	6	1
20	2025-08-06 05:19:31.469459+00	9	lifeplannerktm_am (Admission Manager)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team", "Staff status", "Superuser status"]}}]	6	1
21	2025-08-06 05:21:06.765796+00	8	aektm_lp (Admission Executive)	2	[{"changed": {"fields": ["Username"]}}]	6	1
22	2025-08-06 05:25:33.54527+00	10	stephie_roby_trainerktm ()	1	[{"added": {}}]	6	1
23	2025-08-06 05:27:04.964784+00	10	stephie_roby_trainerktm (Trainer)	2	[{"changed": {"fields": ["First name", "Last name", "Role", "Staff status", "Superuser status"]}}]	6	1
24	2025-08-06 05:58:04.835643+00	7	Operations@Lp (Operations Manager)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team", "Staff status", "Superuser status"]}}]	6	1
25	2025-08-06 06:55:27.002931+00	7	Operations@Lp (Operations Manager)	2	[]	6	1
26	2025-08-07 15:20:29.839575+00	6	suhaila_admissions (Admission Manager)	2	[{"changed": {"fields": ["password"]}}]	6	1
27	2025-08-07 15:21:36.266148+00	6	suhaila_admissions (Admission Manager)	2	[]	6	1
28	2025-08-08 05:04:30.802302+00	11	bintu_admissions ()	1	[{"added": {}}]	6	1
29	2025-08-08 05:05:30.674251+00	11	bintu_admissions (Admission Manager)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team", "Staff status", "Superuser status"]}}]	6	1
30	2025-08-08 05:26:14.467263+00	9	lifeplannerktm_am (Admission Manager)	2	[{"changed": {"fields": ["password"]}}]	6	1
31	2025-08-08 05:26:33.145314+00	9	lifeplannerktm_am (Admission Manager)	2	[]	6	1
32	2025-08-08 08:52:21.491113+00	164	Not Acquired (9048157623) - Enquiry	2	[{"changed": {"fields": ["Assigned to"]}}]	7	7
33	2025-08-12 08:58:27.786094+00	8	aektm_lp (Admission Executive)	2	[{"changed": {"fields": ["password"]}}]	6	1
34	2025-08-12 08:58:50.543424+00	8	aektm_lp (Admission Executive)	2	[]	6	1
35	2025-09-19 05:28:30.535686+00	10	stephie_roby_trainerktm (Trainer)	2	[{"changed": {"fields": ["password"]}}]	6	5
36	2025-09-19 05:28:55.483335+00	10	stephie_roby (Trainer)	2	[{"changed": {"fields": ["Username"]}}]	6	5
37	2025-09-30 11:07:14.346216+00	12	jyothi_lifeplanner ()	1	[{"added": {}}]	6	1
38	2025-09-30 11:12:41.245599+00	12	jyothi_lifeplanner (Admission Manager)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team"]}}]	6	1
39	2025-10-04 06:33:17.960005+00	13	govind_hob ()	1	[{"added": {}}]	6	8
40	2025-10-04 06:34:04.741505+00	13	govind_hob (Business Head)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team"]}}]	6	8
41	2025-10-08 09:03:56.875377+00	2	lp_media (Media Team)	2	[{"changed": {"fields": ["Username", "First name", "Last name", "Superuser status", "Last login"]}}]	6	5
42	2025-10-10 05:10:44.784025+00	11	dummy4 - Overdue	2	[{"changed": {"fields": ["Status"]}}]	12	5
43	2025-10-10 06:43:47.113256+00	11	bintu_admissions (Admission Manager)	2	[{"changed": {"fields": ["Superuser status"]}}]	6	1
44	2025-10-10 06:44:08.78587+00	5	aleena_admissions (Admission Manager)	2	[{"changed": {"fields": ["Superuser status"]}}]	6	1
45	2025-10-10 06:44:30.569485+00	4	aneeta_processing (Processing Executive)	2	[{"changed": {"fields": ["Superuser status"]}}]	6	1
46	2025-10-10 06:44:56.174792+00	13	govind_hob (Business Head)	2	[{"changed": {"fields": ["Staff status", "Superuser status"]}}]	6	1
47	2025-10-10 06:45:29.83156+00	12	jyothi_lifeplanner (Admission Manager)	2	[{"changed": {"fields": ["Staff status"]}}]	6	1
48	2025-10-10 06:45:43.852056+00	9	lifeplannerktm_am (Admission Manager)	2	[{"changed": {"fields": ["Superuser status"]}}]	6	1
49	2025-10-10 06:46:03.058568+00	2	lp_media (Media Team)	2	[]	6	1
50	2025-10-10 06:46:16.603335+00	10	stephie_roby (Trainer)	2	[{"changed": {"fields": ["Superuser status"]}}]	6	1
51	2025-10-10 06:46:34.280519+00	6	suhaila_admissions (Admission Manager)	2	[{"changed": {"fields": ["Superuser status"]}}]	6	1
52	2025-10-10 06:46:46.921038+00	7	Operations@Lp (Operations Manager)	2	[]	6	1
53	2025-10-10 06:46:59.756588+00	8	aektm_lp (Admission Executive)	2	[{"changed": {"fields": ["Superuser status"]}}]	6	1
54	2025-10-10 09:34:05.493215+00	1	rishebs - lifeplanner media - 2025-10-10	1	[{"added": {}}]	16	13
55	2025-10-10 09:45:02.609807+00	2	Anurag - lifeplanner media - 2025-10-10	1	[{"added": {}}]	16	13
56	2025-10-11 06:07:21.87082+00	3	priyan - lifeplanner media - 2025-10-11	1	[{"added": {}}]	16	13
57	2025-10-14 10:41:44.216061+00	5	anurag - lifeplanner media - 2025-10-13	3		16	1
58	2025-10-14 10:41:44.216118+00	4	monday_test reports - lifeplanner media - 2025-10-13	3		16	1
59	2025-10-14 10:41:44.216144+00	3	priyan - lifeplanner media - 2025-10-11	3		16	1
60	2025-10-14 10:41:44.216164+00	2	Anurag - lifeplanner media - 2025-10-10	3		16	1
61	2025-10-14 10:41:44.216183+00	1	rishebs - lifeplanner media - 2025-10-10	3		16	1
62	2025-10-16 06:04:29.195786+00	16	aleena - aleena shaji - 2025-10-16	3		16	13
63	2025-10-17 08:08:09.638833+00	14	ishi_elizabeth ()	1	[{"added": {}}]	6	13
64	2025-10-17 08:09:24.016535+00	14	ishi_elizabeth (Trainer)	2	[{"changed": {"fields": ["First name", "Last name", "Email address", "Role", "Team"]}}]	6	13
65	2025-10-21 07:06:08.286214+00	8	aektm_lp (Admission Executive)	2	[{"changed": {"fields": ["password"]}}]	6	13
66	2025-10-21 07:06:16.264145+00	8	aektm_lp (Admission Executive)	2	[]	6	13
67	2025-10-21 11:22:37.313467+00	30	Risheb.s - lifeplanner media - 2025-10-21	3		16	13
68	2025-10-21 11:23:53.942115+00	31	Risheb - lifeplanner media - 2025-10-21	1	[{"added": {}}]	16	13
69	2025-10-21 11:24:47.377133+00	32	Risheb - lifeplanner media - 2025-10-21	1	[{"added": {}}]	16	13
70	2025-10-21 11:25:32.976788+00	33	Anurag - lifeplanner media - 2025-10-21	1	[{"added": {}}]	16	13
71	2025-10-21 11:26:08.363486+00	34	Anurag - lifeplanner media - 2025-10-21	1	[{"added": {}}]	16	13
72	2025-10-21 11:34:31.178875+00	37	Jyothi KS - jyothi K.S - 2025-10-21	3		16	13
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-08-05 07:39:09.668969+00
2	contenttypes	0002_remove_content_type_name	2025-08-05 07:39:11.409621+00
3	auth	0001_initial	2025-08-05 07:39:17.040657+00
4	auth	0002_alter_permission_name_max_length	2025-08-05 07:39:18.056503+00
5	auth	0003_alter_user_email_max_length	2025-08-05 07:39:18.721705+00
6	auth	0004_alter_user_username_opts	2025-08-05 07:39:19.787067+00
7	auth	0005_alter_user_last_login_null	2025-08-05 07:39:20.804388+00
8	auth	0006_require_contenttypes_0002	2025-08-05 07:39:21.830903+00
9	auth	0007_alter_validators_add_error_messages	2025-08-05 07:39:22.917277+00
10	auth	0008_alter_user_username_max_length	2025-08-05 07:39:23.944739+00
11	auth	0009_alter_user_last_name_max_length	2025-08-05 07:39:25.049903+00
12	auth	0010_alter_group_name_max_length	2025-08-05 07:39:26.843761+00
13	auth	0011_update_proxy_permissions	2025-08-05 07:39:27.536851+00
14	auth	0012_alter_user_first_name_max_length	2025-08-05 07:39:28.540191+00
15	accounts	0001_initial	2025-08-05 07:39:35.523344+00
16	admin	0001_initial	2025-08-05 07:39:38.42011+00
17	admin	0002_logentry_remove_auto_add	2025-08-05 07:39:38.786957+00
18	admin	0003_logentry_add_action_flag_choices	2025-08-05 07:39:39.875944+00
19	leads	0001_initial	2025-08-05 07:39:42.932908+00
20	leads	0002_lead_program_lead_status	2025-08-05 07:39:44.76757+00
21	leads	0003_processingupdate_alter_lead_options_and_more	2025-08-05 07:39:55.080329+00
22	sessions	0001_initial	2025-08-05 07:39:57.127961+00
23	trainers	0001_initial	2025-08-05 07:40:00.089356+00
24	leads	0004_alter_lead_program	2025-08-06 07:06:26.585618+00
25	leads	0005_alter_lead_source	2025-08-07 06:46:24.76598+00
26	accounts	0002_user_manager	2025-08-11 09:10:34.011686+00
27	leads	0006_alter_lead_assigned_to	2025-08-11 09:54:53.618969+00
28	accounts	0003_remove_user_manager	2025-08-12 05:57:23.643425+00
29	leads	0007_lead_remarks	2025-08-12 12:08:55.511854+00
30	leads	0008_alter_lead_custom_source_and_more	2025-08-15 05:23:43.09628+00
31	leads	0009_remarkhistory	2025-08-19 06:16:36.303261+00
32	accounts	0004_alter_user_role	2025-10-04 06:47:08.501554+00
33	tasks	0001_initial	2025-10-04 06:47:13.15677+00
34	leads	0010_alter_lead_status	2025-10-06 09:00:31.130714+00
35	hob	0001_initial	2025-10-08 05:50:32.957109+00
36	tasks	0002_alter_task_status_alter_taskupdate_new_status_and_more	2025-10-10 01:41:37.836359+00
37	tasks	0003_alter_task_status_alter_taskupdate_new_status_and_more	2025-10-10 01:48:12.70416+00
38	tasks	0004_alter_task_status_alter_taskupdate_new_status_and_more	2025-10-10 05:04:28.625963+00
39	hob	0002_delete_dailyreport	2025-10-10 09:00:13.182872+00
40	accounts	0005_dailyreport	2025-10-10 09:17:34.054279+00
41	accounts	0006_dailyreport_heading_dailyreport_name	2025-10-10 09:31:47.564728+00
42	accounts	0007_alter_dailyreport_unique_together	2025-10-10 09:43:37.037207+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
mlt4g9nnq1d8koaladddbokog2t242cl	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ujfFZ:Fq2aKOvlHROlXNbgNKfAJjqmijqe5OduGEO0coH2hG4	2025-08-06 15:36:17.354265+00
mbdytgl6il1krtp3s726m5fnmp2b9vvh	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujdRb:eU_e7qbbwhRbWcEPrBa2pJlnoZV_nN1221UOOB2nXL8	2025-08-06 13:40:35.695155+00
7ai505kqkyohkqpbz37195vxkh5addoi	.eJxVjMsOwiAQRf-FtSFAeY1L934DYRiQqoGktCvjv2uTLnR7zzn3xULc1hq2kZcwEzszyU6_G8b0yG0HdI_t1nnqbV1m5LvCDzr4tVN-Xg7376DGUb-1QoOUtPWuTN5DcoqMlN6BSSUKDQUSCkcSrHHGKkILFlBPXgDoXDx7fwDQyDcb:1ujCMD:kz4Yf4W_b9kV_TjAeLPownfGVsiTnUMuNNDEwGusulg	2025-08-05 08:45:13.753524+00
cao6z0xppld2ymr06l0lgybcawtpe7jn	.eJxVjDkOwjAUBe_iGlle4o2SnjNEf7FxADlSnFSIu0OkFNC-mXkvMcK21nHreRknFmdhxel3Q6BHbjvgO7TbLGlu6zKh3BV50C6vM-fn5XD_Dir0-q01K07FJOUVeOeCtTGUwReEyJAMa-cKIlJAM1CIZAYEHwhRW1KITrw_4PU4VQ:1ujIoa:bfoJDfM3SA32_9vuQvZdUltIWO10RB09mPxUTjPDqOw	2025-08-05 15:38:56.710299+00
fyjhivw56pcgzcucm1b7pydkq7xlzx0x	.eJxVjMsOwiAQRf-FtSFAeY1L934DYRiQqoGktCvjv2uTLnR7zzn3xULc1hq2kZcwEzszyU6_G8b0yG0HdI_t1nnqbV1m5LvCDzr4tVN-Xg7376DGUb-1QoOUtPWuTN5DcoqMlN6BSSUKDQUSCkcSrHHGKkILFlBPXgDoXDx7fwDQyDcb:1ujG57:7DnCP31gEp02BoZFMe-lHPwFt1141Vn0A6OILT54khI	2025-08-05 12:43:49.22799+00
hr2horwcj8r0lml9o6pcnnsl0vo1i59i	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujdrx:4pqWs-5Ba8L7WfB8TYIVtB750HBGelrEwu9OExymPH0	2025-08-06 14:07:49.201054+00
vasa1bacrpz0a3hc16li9ir2v3kkciu5	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujWRi:eAT1J_Egg7CWsz10_K-mR8sGZ5q6CNiWWoBuWYC9nFA	2025-08-06 06:12:14.343857+00
u56g090uuh3eb2obn8eayxxn0joyu7zp	.eJxVjDkOwjAUBe_iGlle4o2SnjNEf7FxADlSnFSIu0OkFNC-mXkvMcK21nHreRknFmdhxel3Q6BHbjvgO7TbLGlu6zKh3BV50C6vM-fn5XD_Dir0-q01K07FJOUVeOeCtTGUwReEyJAMa-cKIlJAM1CIZAYEHwhRW1KITrw_4PU4VQ:1ujG6e:hcU1fRD-zWbP7lb5Xay4je7106bzs33IZPPb6UyiKCo	2025-08-05 12:45:24.50662+00
7tv2sd9o1f6rlsvvk09u33f7d5jg93s3	.eJxVjDkOwjAUBe_iGlle4o2SnjNEf7FxADlSnFSIu0OkFNC-mXkvMcK21nHreRknFmdhxel3Q6BHbjvgO7TbLGlu6zKh3BV50C6vM-fn5XD_Dir0-q01K07FJOUVeOeCtTGUwReEyJAMa-cKIlJAM1CIZAYEHwhRW1KITrw_4PU4VQ:1ujG7t:ZXPXFHapalFaQkwQcFlGAWYIHss6ShcjedM5y1NWX3w	2025-08-05 12:46:41.034201+00
hlic9s1gr7nisau2hsuunwnxlqbadk1g	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujYFb:MxLsS7lhW8j4dKdP9bhVi7yw30d6b1udlrInD1yxoDA	2025-08-06 08:07:51.125932+00
06s7dkr0zuxu0rc5ob3uwwkm695lt749	.eJxVjEEOwiAQRe_C2pAOdBhw6d4zkOlApWpoUtqV8e7apAvd_vfef6nI21ri1vISp6TOCtTpdxtYHrnuIN253mYtc12XadC7og_a9HVO-Xk53L-Dwq18axKPSCjMXeiyoDhg8gLBsoNsx9FSANMjgbVsPBL5jM6HFMT0xjr1_gDIxDab:1ujWg5:BZ1-AuIn47Fiv0n-mp-9sQL__7aSKrvkl6Rhbv7HzIA	2025-08-06 06:27:05.849768+00
5ierhsxsd9jh5j2xbkcu3dlu8w6ant0a	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujJGU:QaWTXNySdmU-Z7gj8jovkMmQW0VjUH_WlFcM5sOPGlg	2025-08-05 16:07:46.255604+00
d2v8m7e8rlp3t8ldag9t8q0ki0286n1t	.eJxVjMsOwiAQRf-FtSFAeY1L934DYRiQqoGktCvjv2uTLnR7zzn3xULc1hq2kZcwEzszyU6_G8b0yG0HdI_t1nnqbV1m5LvCDzr4tVN-Xg7376DGUb-1QoOUtPWuTN5DcoqMlN6BSSUKDQUSCkcSrHHGKkILFlBPXgDoXDx7fwDQyDcb:1ujFoz:bJ3loIMRuYIzWCwgeMbubffN3eteRK0FNy1Wap-D2Ew	2025-08-05 12:27:09.968458+00
uqyxmsxllobn5diyfu39k9sn1r206jnc	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ujYpQ:h8Gqtgfoux-jzghpU8qa45CPcVKKyYhpCux-Zq1qmzo	2025-08-06 08:44:52.969979+00
4wuwckcek9rx53ewg8e8trur2iwa7ktz	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujuPF:ZCs_5kzOm5C6CSPR042MfvKtycz-DvWReC0yEI5P2uY	2025-08-07 07:47:17.832734+00
k8eayafsa3fc26ine57vs43e0zei7i2u	.eJxVjEEOwiAQRe_C2pAOdBhw6d4zkOlApWpoUtqV8e7apAvd_vfef6nI21ri1vISp6TOCtTpdxtYHrnuIN253mYtc12XadC7og_a9HVO-Xk53L-Dwq18axKPSCjMXeiyoDhg8gLBsoNsx9FSANMjgbVsPBL5jM6HFMT0xjr1_gDIxDab:1ujY3c:whTka-zRzhcIW75i59sg5dmS_0qxElHycnFEKMkX3iw	2025-08-06 07:55:28.117545+00
tenpktwrt4mvi1i7bz9bai7smofnh2gr	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujYpm:3Z1PAaNFdR-9qkcZ7o51ljRQWBHkWEu_EIls5B6lGcE	2025-08-06 08:45:14.866726+00
40t1nu25yxpfht4h4exryd2xdncrvg9m	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujKiZ:DCD-yckLLZ5qFe-Tz-vnaQH35nPgVRmxccnbI5Gu5To	2025-08-05 17:40:51.388961+00
aa8ftedvnlkzweqx6n1kjbse0uo4q2r6	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujL9m:HryLIuqpSzcTMytTnAj6xpj8lzdteAz0Ggt6w63RoeE	2025-08-05 18:08:58.648664+00
6lfs7jqwlrzthx3s3anodlza4immptyw	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujsHx:HAj_VmnizpincmFaFA3U4iDruXxrO_SV6ocE9bGUJWY	2025-08-07 05:31:37.496555+00
0jlik5c2s8lpquuyrdg5dgcxxkeg7fyw	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujbxg:Q64Ij0zThFB5IMUvuXRGDLXhoc1cuXMVpUKsDz-mJT8	2025-08-06 12:05:36.197765+00
k844v22jwx8kma76iyug00jr11xdkqyj	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujViH:lechYUYvCK194XSUVC9nAQVq9PRzzk7WBn9c4vnyRu4	2025-08-06 05:25:17.306517+00
jfn4q46xf2nx42h0veqtzqpp7zhmlnzl	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ujXwX:3h3yKuTvThQvuf5xyl2Qoaa0lFtGLgb1g_AeOz40JX8	2025-08-06 07:48:09.551558+00
qg3evur3kd5ia3ku0mdfhonn23momul1	.eJxVjEEOwiAQRe_C2pAOdBhw6d4zkOlApWpoUtqV8e7apAvd_vfef6nI21ri1vISp6TOCtTpdxtYHrnuIN253mYtc12XadC7og_a9HVO-Xk53L-Dwq18axKPSCjMXeiyoDhg8gLBsoNsx9FSANMjgbVsPBL5jM6HFMT0xjr1_gDIxDab:1ujWA4:nqejOBlkLeLmSyC8XgEVqDoLZ-wq8MZRRiX705H25Wk	2025-08-06 05:54:00.580908+00
hlegdjyhuwsids1p4or0l183c4uhjlt3	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ujYPp:2GXh-ufmDjtJ5V1tGeSY9Oyu7G87KnMX3D8h23RhIIQ	2025-08-06 08:18:25.234573+00
bb9e91d0c6qeby5igbj3qc86zwus6bpj	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1umvCQ:E8r94SYmrxXux6njfyCOZP1MV9lA4hiDDe2yL0bAqr8	2025-08-16 14:14:30.291026+00
pup8fswya7nwaopi7awx3bf3jo02q1jv	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ukHB3:hoouZssv1sKZ02gJ2q5JwbuiecQOQZY3pSLDim-OpEQ	2025-08-08 08:06:09.425061+00
u08wk18ipmsm10n4i1morhrdlmtrs2x9	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujtpK:IwhLJqlQSHe8isP7hw8yRHzcXLrUxrHt3oHfa0jUBj4	2025-08-07 07:10:10.296229+00
kc8o5gy8veg76qavrthaim4h1871z2gm	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ujyt7:dXDhUFM7vXdGe0GfiQ7AOScn2p4Ao_jTFd6wOFvByuQ	2025-08-07 12:34:25.492615+00
zuin2us51qibbj8011ehyv3orv6jshj4	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ujzO4:9Mb3KDqz4TCagvVnAmIauqt2b7ALW84-G5n3UPyUN4U	2025-08-07 13:06:24.971022+00
s1szlfj0br715x963issedfiwa183pkf	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ukIqh:t1ebdQNdQ4uvFQIBRnT27ok5Tt7saNpB-UzHjN0Ai9s	2025-08-08 09:53:15.595088+00
zn0gfbrynxeiv3qrzu08g2s6ftg1q3u0	.eJxVjDsOwjAQBe_iGlmxg3-U9JzBWu-ucQDZUpxUiLuTSCmgnZn33iLCupS4dp7jROIizuL0yxLgk-su6AH13iS2usxTknsiD9vlrRG_rkf7d1Cgl23tbQJGn40FBs6DC6Rt9qh9cCNlk7wayLnkTFAGR60MoLIcBiS7QSM-XwG4OB4:1ukLzA:lBO6oVJs8FLWeezyniCbMxgNrZ_yLEIHpkpsxX0-bU8	2025-08-08 13:14:12.434969+00
wqpln8kojlya1trjnek2td0y5xyzr495	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ukhrq:B4UyOSm7YKfRXaPhBo0O-HuYAKpwsfRUDLGpF3iQMrw	2025-08-09 12:36:06.167406+00
7p6tx23keewq3o2jvf4xwt34e0bn849j	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ujfFP:PPUzuVUnQEyqrjZiqo0y3R79hFc5rHDW5qUpegBwLzA	2025-08-06 15:36:07.828949+00
wd4hkjudu4w7hhes6v2y2vpvepnah7i5	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1uk0o8:SjfS4mZ9mRtsPe26USLjlmsdRL4qm8JobNu2xIF9gxQ	2025-08-07 14:37:24.732164+00
wpfsrae9sf0revaw0sw27ahif3yfohpt	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1uki0M:xYasN0R0oT5KY9Wi-UmOttj2JycJEG8VQTl_7aNfpco	2025-08-09 12:44:54.811111+00
2kuckpdsewkvd1zyz0nwz27nfa1ygsi7	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1ukJuQ:2-8FQ7D7zl9ttCf6bHS5gHzwa5jt4WU7qKgMA9lxv5c	2025-08-08 11:01:10.978085+00
3tbgs7g3wio3xs18y10bnmn5evjycez5	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ukI7b:eh883UFPCHyqVJTi1r5jC2M7zWjyo4ZE6BzFxbIBzoU	2025-08-08 09:06:39.199745+00
8z7bh1tg7alqsjoa7fnwb2t35aaodq2c	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1uki0n:6ygiXR8Ho_yPkbrtTOsBILSJ9gVXNLRA_tPVVIfQe9k	2025-08-09 12:45:21.968621+00
9xzx51eg071or18vrci7tplj1uxoy6q5	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1uk1Dm:B1i_0dAZ_d1GhwZStskocmt6AtNixAcelLL1GANnQOw	2025-08-07 15:03:54.858842+00
7nkvck7l6xj2kb6mjourqjruf8yt3ytr	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ukFkZ:_DCkb4vkYC9dY-LYmACp0DK60TVM0XnN2tHpBmaZtok	2025-08-08 06:34:43.861452+00
c32thra2xgdkaxw3z9ntoyelyanvatpa	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1uk2n0:h3QumHSoqqEvi1azGA2sTa0to72QokTqeaY035N9zMY	2025-08-07 16:44:22.641908+00
qmn11gk3v8wvpmwwb5q1ymkacp1ydkw8	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ukKED:YZw1bPvfJUJQipGlJJ_0EorMRlT7lViefcbW05okPIc	2025-08-08 11:21:37.083534+00
5s37vj8a9hwrojcjwdum9lc0onj0awm7	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ukFoz:9kLYN5ULrcy8q1X0x9v8zvGXOFSA_Te8deYo40J4zUM	2025-08-08 06:39:17.086091+00
axxzfipsoaxf08geav15mryl8f4wcfns	.eJxVjDsOwjAQBe_iGln-fyjpOYO1Xq9xADlSnFSIu0OkFNC-mXkvlmBbW9oGLWkq7MykZKffMQM-qO-k3KHfZo5zX5cp813hBx38Ohd6Xg7376DBaN-aNGVHxSrEWnU1YHSIKgorowFnqvNBgfIkolVBoqDoyRLoitJodMTeHxBNOBM:1ukFq0:6__TKGvjHLqIIxXXTmmGWCSMU9dd1LQhskn8uLF-1j4	2025-08-08 06:40:20.6849+00
en9we2eyfwkqbfm0akhrhfse5134cbl6	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ukGdI:SXMPNDesEawVX2LniBcor5iPovnlhap-t_xi954d3pQ	2025-08-08 07:31:16.087377+00
mv6yfnzc3he0call28mhc4y2syrzutgi	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ukKqI:skRH_MfHAADYquTQqKmjJOI5bb682YWz-As8xV7OlM4	2025-08-08 12:00:58.394271+00
of2qc8qpnwgpnrynhzma99ivyz621r3s	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ukGrV:aXJnaox56WZxotTdXTEzyScFN6AMSA5gt-2UnEt6rXs	2025-08-08 07:45:57.46563+00
o6xlri31kv3kph5auzankd6nwf9tuf0y	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ukhiM:iT76p54FZjDFcAH9hwtN72zOy3QNcrZT-7lfgl7zBIU	2025-08-09 12:26:18.837014+00
vff7fgdq4yrk9xlo3h4ztbpbhefjw2ll	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ul1ag:hBABLWiMmd_mTEeDoUa4kc7jsR2-zAs8FSsdg8vINe8	2025-08-10 09:39:42.325429+00
67be58sgol84g2ikmtenqhv73v1wu12m	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ulMqO:vb2ZEFbV71wWnc6Z1ExD8vCekYO9kjBWFdhWWjF2Zo8	2025-08-11 08:21:20.708828+00
3cy2m7syr741kxeuk4a1gjp14nfth5qq	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ulLr6:ieqCBE4dd4x-EW0sSkinhRTR0jyUPo--N2GESPcQOww	2025-08-11 07:18:00.601489+00
4jllfkf09g1kvh379w463uy8fsjqiweg	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ulKdC:eCDAHgiq2SxRhWBpxcKWTCJpGI4ChuDXy6EmwBzTKVI	2025-08-11 05:59:34.404228+00
v0n0l65p8zy5lotko5pg045b04wp3zbz	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ulmmX:wyR0hkpmeQGtY1G4uO-5Pwvx8lY-Is44UPFeph8LEro	2025-08-12 12:03:05.039682+00
ahpt812oyzi3u4v5p1cp9r214ttueb6b	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1uljFR:vx1USM2yHRdKdjvEyrNhBHHIxZ5QCJyP3BU2pehdqbE	2025-08-12 08:16:41.007022+00
zsstqqem6udnro7yfmgfa619znxhabpu	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ulOah:KxjhP3k46jWyCqTOL3j6fSz2Ap46Ny420RakMM21k-g	2025-08-11 10:13:15.167927+00
unjs0odkxm979chefta5qr8r9gid6mx7	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ulLbl:UWQ2-ZUvPUz4NOaPtNVeUhRFu_aU8_TFH3AwLqLqCNg	2025-08-11 07:02:09.567008+00
8bekjpee9qg9fcigr5flmupjl3h9bhia	.eJxVjDsOwjAQBe_iGln-fyjpOYO1Xq9xADlSnFSIu0OkFNC-mXkvlmBbW9oGLWkq7MykZKffMQM-qO-k3KHfZo5zX5cp813hBx38Ohd6Xg7376DBaN-aNGVHxSrEWnU1YHSIKgorowFnqvNBgfIkolVBoqDoyRLoitJodMTeHxBNOBM:1ulPk9:vrzhR3oNOjFsMm9DU-2bICxJO8Ak6LRt3ZqQ9NkOgyA	2025-08-11 11:27:05.021834+00
0l9jr0xyxk0x0sf5f1pfttfw13hldhym	.eJxVjDsOwjAQBe_iGln-fyjpOYO1Xq9xADlSnFSIu0OkFNC-mXkvlmBbW9oGLWkq7MykZKffMQM-qO-k3KHfZo5zX5cp813hBx38Ohd6Xg7376DBaN-aNGVHxSrEWnU1YHSIKgorowFnqvNBgfIkolVBoqDoyRLoitJodMTeHxBNOBM:1ulkYK:CzZEIN47n2A1kyfnNTBNplucxF-LNoJtUn8tqHlwzW4	2025-08-12 09:40:16.450815+00
mep2anff378lcgjn413rzmfhg4mqpiee	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1ulmpc:R0VyDJ4fRVklXX6QRdWY1fX77ZkH9ZQVvxd09OGsIYc	2025-08-12 12:06:16.454801+00
04puz8d8go41749o89vbtogtt774hd5p	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1ulLma:1ciNqE1uk78-OUr6vMxnurzLb4pbR4azS2GEqoFvXBc	2025-08-11 07:13:20.164448+00
f7tz6xyfd3xhlba1a6kzd71ztqcv1wn2	.eJxVjDsOwjAQBe_iGln-fyjpOYO1Xq9xADlSnFSIu0OkFNC-mXkvlmBbW9oGLWkq7MykZKffMQM-qO-k3KHfZo5zX5cp813hBx38Ohd6Xg7376DBaN-aNGVHxSrEWnU1YHSIKgorowFnqvNBgfIkolVBoqDoyRLoitJodMTeHxBNOBM:1ulhCE:FQ-CRkBS7zf0NQ58a33MzSz4wgpR6aDD3A6gp-dVCBc	2025-08-12 06:05:14.933646+00
tulyg3qt4g76gbyv9gij239fvzmx4q29	.eJxVjDkOwjAUBe_iGlnKj1dKes5g_cXGAeRIcVIh7g6RUkD7Zua9VMJtrWnreUmTqLNy6vS7EfIjtx3IHdtt1jy3dZlI74o-aNfXWfLzcrh_BxV7_daG2cBIkRi4OAjoIwUg5wWicRiMUAaKsYTRehlKyLF4O4Az1ohFVO8P7rM39A:1ulM06:otdzL-v6dJmxVtXsH8e472AMnhvAVBCCGag7srj4v-I	2025-08-11 07:27:18.961119+00
c6z64jnqwfojxz8yeqnsktzu2xs1mx20	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1ulLnv:tYzWW4uCVi-D_CyOtxDW2r1thtZH5sRraXMXtFnXG4g	2025-08-11 07:14:43.969742+00
p8opqo79h7ru6b16bmtgz2os8m03ta3r	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ulMLw:NPQMJoWjsthqqJHcixwwN9P1pROiUOP2FqywkjL8kJ4	2025-08-11 07:49:52.264258+00
gdccq5ttag1q71djlknmhzat32ubtd1j	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1ulmiz:M_TBZvhTrNo1Du1wVBfuJ64oQlOR6fzLeKt1AMnoGYU	2025-08-12 11:59:25.301683+00
dufnbn4ozp2wt0u3j4gyrr6v5xb9z1aa	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ulOET:YevA-DiljuaKHlhz7xlZtSKP3d4x33Or1xSs6Q7Ba3k	2025-08-11 09:50:17.131835+00
8my7h3ogrnd6f9yv6pewqy5456d9pzr7	.eJxVjDsOwjAQBe_iGln-fyjpOYO1Xq9xADlSnFSIu0OkFNC-mXkvlmBbW9oGLWkq7MykZKffMQM-qO-k3KHfZo5zX5cp813hBx38Ohd6Xg7376DBaN-aNGVHxSrEWnU1YHSIKgorowFnqvNBgfIkolVBoqDoyRLoitJodMTeHxBNOBM:1ulLPa:evG11o3U2EPLKWM-cFOmUrFBbTqOCY52X8XdZjDLk9Q	2025-08-11 06:49:34.561521+00
cuzf0y70j6dmpb02wwvi8q38gmovs1is	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ulhSz:_iK7W1SsjaLtLZOKFAZ8wnRvKEsvETpZz0cZR8DUB3A	2025-08-12 06:22:33.392662+00
0r5mqswavs8nw1wszbvuw1iyhinr0m34	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ulQoy:8baW-sP5mMimEhvlI-bWITAQYRltLJytn8vbXv-tjt4	2025-08-11 12:36:08.110249+00
9lrz32cgppdepwlfk6s77dh2eke7ylbd	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1uli3G:N20MhoI0JdYs2QQXETra68rD_sBZZ7gd-VQqOUsD644	2025-08-12 07:00:02.3025+00
rv610rzw2ys2xvixbr0ofsc5c7o6o2p6	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1ullBO:fFOPtmDdM4QCpdyby6seMAqceqDlNeKahWuOEdjsEvU	2025-08-12 10:20:38.795911+00
na15dyme12ot2sxnlehzj1kz44297mka	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ulmX3:HmsW1nPDLhCCjtcrYPDdjWQaL7Y1WCUdVXkKmL-0SJc	2025-08-12 11:47:05.278159+00
cw2jf5d5oj5oc3sta01mski5b58g2ux2	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1ulMp3:MsqhzlM-CsXIewnvZ8JGydO7_zujcxjnERX1XIaLoUI	2025-08-11 08:19:57.781976+00
kmwi0fmpu2h45sbhzgigga1mq2ds2k36	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1umVSO:jayVSQd2RYGQ-zcKsIi7WkZcvVLZd9VKO06BNc8yjhg	2025-08-14 11:45:16.704958+00
jljuizzqg7pwugx7zlb3v0h24o1cifl2	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1umUZx:vXhmKq6X_v69wALQ0b0wUF0EFg4_K3cdV122KETnI2k	2025-08-14 10:49:01.974825+00
8ahqq5omr6s4jlop1ajhxjkx2wxy3wgp	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1um9Vn:65nTTJ8DeQ3I3JXVV7zSVO_5NXPBhLuNfWX3CGY7YYA	2025-08-13 12:19:19.294509+00
eph2da6gghqvii3ol2lk8vdrktm3dgsg	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ursak:B3PNYCmzlQ854UNJc6koCAa_qNGCHhCx9GlbjP0TIdU	2025-08-30 06:28:06.663568+00
29qvmwbadxy4uv8a84tkgs1aufl6ossg	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1unEq1:YECBaswhN_jErvzd6wl7wIwviYq3tQtyZzmmm97Scz0	2025-08-17 11:12:41.542381+00
o8i9goyv8t56t30zrtfrwvwhwv5wv4yx	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1uyore:ShxE3REpmqSdvP4Kvrp09o8bITslqZsnKOtcyQOWclg	2025-09-18 09:54:14.17729+00
wqibr9harjc7qusjghgp16cfeu8k2giu	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1un95E:xoJDJIdWmv1YmIKzOya3NwIUfevrBWEIHy5u0yGtxZ0	2025-08-17 05:04:00.464095+00
517zfuedwefow1e59r0i5mivadbbf477	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1upJFs:jsx8rl1telz9ywcpVNJ9sVfjUytXbrU-iJGKChQDKZk	2025-08-23 04:19:56.153672+00
f0i2vprkbxuobs2q3pj7lgojt33igzky	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1upPMH:RZtm8K2RS872TTbDyLDL_BheoPedWtboU1uJuqUKCw8	2025-08-23 10:50:57.523884+00
vfi0u1ydxqzxn8hfct7ht1pt66n7taz7	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1ulu74:hGUJbFL8kQAvseqG_bPB-ncP9VBNs2yaJ6iqtGLJZw4	2025-08-12 19:52:46.620927+00
l7e6tgm707poz05k2h604j0ktutvscbv	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1um9dW:9y2xvwgXBLs-IfysF70k1yNd876Vm9qfmOkPWtl00Sc	2025-08-13 12:27:18.422406+00
7y4ozuib7mptwirzyys9wkn9tt4iw03t	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1ulu7B:sMiqT31c5jGDMnK-MDmGSsQ6F9hhwK2Vb6nPsFEoO5E	2025-08-12 19:52:53.174826+00
e2u7fl92hndxdyd06k965aqcpd5mzo0m	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1uoSf1:GAyDMwCsrdcoqu-g-NoWrf4VLMhxgoCM69vd9m_aO5E	2025-08-20 20:10:23.799036+00
v592lum82l7kllqjloj4i0d57ec88yhe	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1ummwZ:cesHXw2OhMLvw0KIaMN-Vjm2h26qLZLl4p3Kgx0ystk	2025-08-15 06:25:35.29969+00
nvf7agne82ohq2erm8jzpm135gnk2vzv	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1ulo8i:4D5xIasovcIHJTNUFsRzN12zH6tZiFW5UiqWy5OTBYw	2025-08-12 13:30:04.20861+00
aika9rcee664zxclhlhva2hru76r1a6n	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1upPPf:kXVBPqBOk5bjsR1sx1VlboOL2T1yK79n1DtKiHsN7Ko	2025-08-23 10:54:27.255942+00
b6dtrmslivvi86aeucadjd68i3wy6nf8	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1umw4K:Ql2EfpYRecDc3IVj9t5rApzT0zqaD0lruIj23GE8puM	2025-08-16 15:10:12.891621+00
0gh3pvf5azz9upo3y3eckd1d0qurzqj5	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1unx2D:moXBM1B_QgV1MG_R0cX9s0gWgdUrbcNT2w7VuOSIIxk	2025-08-19 10:24:13.597269+00
iuwfwnomkt4rmslipru2xyk2slsp8z38	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1umw5m:Qcsp1XnU9LDK0HHbFrv426In3DKn47My06Enwqcc7iY	2025-08-16 15:11:42.164343+00
ahs3472ccmza4o50b74xlyto5w0y3e7i	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1unrAY:WFB1d-MIkZVPwyeFVRtoZKZpn-CRhYKOKEKLfmfUvrw	2025-08-19 04:08:26.873723+00
7ipo53y4ae4kxpseaie16ed36xlre1hs	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1upji1:U9z2FGpPmaDaMgZeKwQ-ggpBGF7Ellsqg1SS0yk0QwY	2025-08-24 08:34:45.698248+00
k7jg36p6odwu9ee8i239v737jf69e2ij	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1uneCN:co6Y0ZZ6nD-cS_-_CcUVxV4TLJXodUNx-r8GxYUcF_0	2025-08-18 14:17:27.208751+00
zr9qjlx9inrupkmelf1naxtosc8fvofy	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1urCif:w6ygqD_y28xtR1KY7GNa3MWQk3406vN4e2k4DGaLyZM	2025-08-28 09:45:29.815991+00
alddgxi5vk87rwzg4guijpzfn3g2ow6l	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1uqWn0:HA-ooaD4dB38zTydUki1r2xail_z0opFtL1q63pScVY	2025-08-26 12:59:10.346197+00
7abhrxnl2nevkbagxsbmd5t2kjhehlpn	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1uoGj9:h7BZFjDU-u3i3Cr1ccgBgdZxG0ykpgc8ULq8YwlUP3Q	2025-08-20 07:25:51.138036+00
oqvlqor032n17vewpdfk1jqfy5zsdzd6	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1ulqRV:PaUPYzzqfUMJHsyZ_BfAFVSK4LP_jeHVXrSTOugmOJA	2025-08-12 15:57:37.578863+00
p7wrk1ijohmub9apmi31jg11mji1qox9	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1unh8H:1Q04siJ20GSiOQ3UPRb_TMvNi5YPjIcAw-prsuUCJE0	2025-08-18 17:25:25.497324+00
cprz5vo3h2mth94yk5wx5a0nht1k1edf	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1um3BO:JF7iF5SdC9_VRRtZOxlmIeWhnkhKdXEHg0iIJILv_pQ	2025-08-13 05:33:50.282539+00
krknkumpkf48h89bb4riu33fdvlx44rl	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1um7rC:6ZfeSL-VNaJiU9WSaw1IrqpNT7OtfHH4fQXuH73_8Rk	2025-08-13 10:33:18.794776+00
7urcki0m7rnc9ir64wbvgroiq7ze3mkr	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1ulqRo:D2PUJFsUDydDcJDr7i7PmheHXuuURfsJaiCRBIgImbA	2025-08-12 15:57:56.83727+00
98l1wbrspiqovdzy4bxhamgm10uid3wt	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1uoaGU:sUr1gwy5W2NUgn5phhKUu-GHkLkx-oOeLZQJiDgVv8M	2025-08-21 04:17:34.355451+00
3jt39q38uzaoer6d7hlqowip2khgtl66	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1um7to:lJvgpSw2TGuKPk9WzJuqtVVP63FWSD2AmS7VTHhYTAU	2025-08-13 10:36:00.665896+00
u6p27jyit39qhi660ok6mqddd2q03kgt	.eJxVjDsOwjAQBe_iGln-fyjpOYO1Xq9xADlSnFSIu0OkFNC-mXkvlmBbW9oGLWkq7MykZKffMQM-qO-k3KHfZo5zX5cp813hBx38Ohd6Xg7376DBaN-aNGVHxSrEWnU1YHSIKgorowFnqvNBgfIkolVBoqDoyRLoitJodMTeHxBNOBM:1um3tx:PifwdImf1HqpEq4L6rySFO7HB_0kfVjtjLRumpDsjZ0	2025-08-13 06:19:53.798412+00
e98c3tuwj812zt1it5w5h9d7xy59dgas	.eJxVjDsOwjAQBe_iGln-fyjpOYO1Xq9xADlSnFSIu0OkFNC-mXkvlmBbW9oGLWkq7MykZKffMQM-qO-k3KHfZo5zX5cp813hBx38Ohd6Xg7376DBaN-aNGVHxSrEWnU1YHSIKgorowFnqvNBgfIkolVBoqDoyRLoitJodMTeHxBNOBM:1unsQM:XrRSGWonmbffWEV_Zt2EjVHjYI5D-O-z5KyOAmPcpzE	2025-08-19 05:28:50.488756+00
ckylup5vcoxf5wjtyn8ozt15ta4db4ta	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1umPJD:Z4RSVLID_KLEmgug1Bz9z8hv3-GxGg3ebZxqfW07EO8	2025-08-14 05:11:23.094971+00
ctos1iawbvjbcems33lfdvgecf1n2hi3	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1ummq8:jAbmshiihU8_bnjy07LNZPyffLOGsK9LwTuAYE_5mU0	2025-08-15 06:18:56.686931+00
6x9qwqa244zjn05k5e9pivvenbxv5ndd	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1umQLH:0VLyiFA-Ig28Sy5PfP0zSrEOO-UhrAyHW37mxgnm0xw	2025-08-14 06:17:35.030723+00
09b2r4o7dhukjpe73v7fibbzzefk48c4	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1umVYW:JCs8fFe4ohmxQ1_6BS4xQU8P4MmdSo1NuL0g68NAHTE	2025-08-14 11:51:36.646814+00
gjtygywvm6kba16fy4ykehhsnd0gc8w8	.eJxVjDsOwjAQBe_iGln-fyjpOYO1Xq9xADlSnFSIu0OkFNC-mXkvlmBbW9oGLWkq7MykZKffMQM-qO-k3KHfZo5zX5cp813hBx38Ohd6Xg7376DBaN-aNGVHxSrEWnU1YHSIKgorowFnqvNBgfIkolVBoqDoyRLoitJodMTeHxBNOBM:1umTc2:_Ofm99lGpHHDnQrTisEVc9CXYqu_B9-slFd-PEzcTfk	2025-08-14 09:47:06.607785+00
u59qjqkqvsot455dut55ydhqji2lk9mq	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1unwCy:aVs4bhkniszx4wo02sKhbxveaThYXE9P0ncDE1Sc1bg	2025-08-19 09:31:16.643503+00
a8bgquvlouffe9hig0dbel825cam75ck	.eJxVjDkOwjAUBe_iGlnKj1dKes5g_cXGAeRIcVIh7g6RUkD7Zua9VMJtrWnreUmTqLNy6vS7EfIjtx3IHdtt1jy3dZlI74o-aNfXWfLzcrh_BxV7_daG2cBIkRi4OAjoIwUg5wWicRiMUAaKsYTRehlKyLF4O4Az1ohFVO8P7rM39A:1um73D:HEsqurRKEjmbf4r5y4fifiqRYzOsVXtPA2JdPSH8Ahc	2025-08-13 09:41:39.176043+00
y4hcs1znvjdkhjlbdxw2z29fqdqgs8ui	.eJxVjDkOwjAUBe_iGlnKj1dKes5g_cXGAeRIcVIh7g6RUkD7Zua9VMJtrWnreUmTqLNy6vS7EfIjtx3IHdtt1jy3dZlI74o-aNfXWfLzcrh_BxV7_daG2cBIkRi4OAjoIwUg5wWicRiMUAaKsYTRehlKyLF4O4Az1ohFVO8P7rM39A:1um73V:AfLDrVBLroxGLBo9qboB1KpqgY0oq_Vr2pocgi2p3hU	2025-08-13 09:41:57.372707+00
1w6mmvt2jnf4bdrs5rh2piuom5ylrbay	.eJxVjDsOwjAQBe_iGln-fyjpOYO1Xq9xADlSnFSIu0OkFNC-mXkvlmBbW9oGLWkq7MykZKffMQM-qO-k3KHfZo5zX5cp813hBx38Ohd6Xg7376DBaN-aNGVHxSrEWnU1YHSIKgorowFnqvNBgfIkolVBoqDoyRLoitJodMTeHxBNOBM:1uod8M:H1SSC24qGHvowvcEi9toABlDNSz9PTP5mXrdnUc5_88	2025-08-21 07:21:22.69848+00
fu25g516ygng9n6t85uks2vn0ar49vkz	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1umVjG:YInb5I9zkjF8LRa8W5AgGVdt6emUWGmkDc6jzI0x7fE	2025-08-14 12:02:42.228504+00
xr2k5k9f5g0r0opscs3c60cdb5mnn9wr	.eJxVjDsOwyAQBe9CHSHA_DZlep8BLSwEJxGWjF1FuXuE5CJp38y8Nwt47DUcPW9hIXZlwC6_W8T0zG0AemC7rzytbd-WyIfCT9r5vFJ-3U7376Bir6OWUqC0oFAUhwZklkUamIRPhnQElXTyTtjivZ1QkDcDgSYXvXIG2ecLxew27g:1umn1J:w1168U0zTDBRhLat36jVAfVm2We6Jil86DT2P0NS174	2025-08-15 06:30:29.897002+00
4ohfdl8luvwwbfcfdlpf43ke1lsts10q	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1um7nH:EsDMzXV00ZYw_vg6NFNV9KojFDZgwUCuQEyG7kZfoR8	2025-08-13 10:29:15.454054+00
z3ungajihn3xigekx3izc3uaw7p1ocem	.eJxVjDkOwjAUBe_iGlnKj1dKes5g_cXGAeRIcVIh7g6RUkD7Zua9VMJtrWnreUmTqLNy6vS7EfIjtx3IHdtt1jy3dZlI74o-aNfXWfLzcrh_BxV7_daG2cBIkRi4OAjoIwUg5wWicRiMUAaKsYTRehlKyLF4O4Az1ohFVO8P7rM39A:1un9eI:s5a71BxA8QE_wvpXWtVw2J-sANu4wpJ8qqd96ROs1uo	2025-08-17 05:40:14.686453+00
57fblqi293zv0razzyr0mggq4zw2bp4e	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1un8nT:Sv6GibTcqGluc6CBZvNJ1RrTuFCLAXy5T_-NdGezyEY	2025-08-17 04:45:39.571854+00
hx0hfr6klb6u482tj18t957a9g7vv32n	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1unsOh:_XL18RUhLvZtqgGtGiPjZX862Stn0AH2-dYGsaxR_sU	2025-08-19 05:27:07.817872+00
vdnc5bmlh6j1zwt8braiica0l8kplop5	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v75Nm:NjvGODgW-UcjLbvtZtJ9Y8XtaZywvsVuNNLDR_W9sQA	2025-10-11 05:09:34.227379+00
13xce9c113n42bgkieu7vhtyqom0hzck	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1v3vOY:IKBcZGXehSeOTNlJziU0tv257CuKI3VJIg5n4pqxBSw	2025-10-02 11:53:18.644657+00
k19t3mls9zktls9gja0pdp2is9xzvawd	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1urc6i:wINLL2fSpjHYW85yofafYYIEU25E-b1RNbE1udi24Zs	2025-08-29 12:52:00.660495+00
0vq8w7spppvw7mmtn11h4y9cgp287nmd	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1v3vPW:mfW9f2WEtSKxICjb7eC_FKgUo_1Dhdatixp3QN7-dN8	2025-10-02 11:54:18.492212+00
v934kymi9ze9b1n4ogd0wb78zj5ch6tk	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1uodb4:VnD4thNx8IijOSH58qRixiYd6hfzC2AAc0FB482HvHY	2025-08-21 07:51:02.557592+00
56zodhuy7ge82g8b72fhftc30gs75hdr	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1upiLh:Z5H-QzVCmESww2J0P_rLc5ZVqlU1oGphZuY4Dbue2PE	2025-08-24 07:07:37.556195+00
nieckzzy2q1cg12ga6inreavhv7fgw7y	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1ulsLZ:bHAa58iyLBqyObACOlQsFf9vEKhuMgBMOq3m4qgVcLw	2025-08-12 17:59:37.211774+00
6cjxtbys0sv6kbcr8w405czvzfwsqptq	.eJxVjDsOwjAQBe_iGln-m1DScwZr17vGAeRIcVIh7k4ipYD2zcx7iwTrUtPaeU4jiYvQRpx-R4T85LYTekC7TzJPbZlHlLsiD9rlbSJ-XQ_376BCr1tdwOdSjMlRW4gUUdOAGsyZyTofgynsNqEMwTnGGK32wSMptKgUZhafLytLOOw:1v4cxR:qtGe7FGBf6Mt6WpsbSzSSAIURbUK0qPZIhlA58uRZPA	2025-10-04 10:24:13.134666+00
gvwx55x4i23c9nr3hwe3i6hd712ii80f	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1upoCO:kyyTOiQyhRNcb4_zgX0w7eBbYCntG5IlQJ1-Tny3ONA	2025-08-24 13:22:24.617917+00
zchaoio5wi8np3m2c5gbimbauzv455w4	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1usCu6:9Ro6kCOyBNt0l_OnGwqQz9mA2oyz24NeCW-DsX4dmfg	2025-08-31 04:09:26.530688+00
7b3fk1g0833696pmyax8ol3ponl3gsks	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1v1ijk:rxFoesEavyoRRb2t8_Z6ulJn1d18WkJm7w_HO6I4Sfg	2025-09-26 09:58:04.656154+00
dv14884xdo3dzumtwqaena3fvw6493r8	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1uoHRb:UhCWfJyyWNEnNH0gAuUFK1g7v1F_y98ZZPyJH35AcNE	2025-08-20 08:11:47.659286+00
vjtge0ximuvyacsgqhnapeerfq6sfdho	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v4dKa:tW-Etw-lWU1WlpORclz87YjJXTxUoIks8fi9zj7Qwrs	2025-10-04 10:48:08.66504+00
t9gwguj7nxmov8159pedctbrxwbbvfrt	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1utgcr:ySQHu4Uqi3LQJbH1rdf_HeNRqvHjzAy4Ry0Gclgdor4	2025-09-04 06:05:45.553558+00
4emogykopqetch6zjks87kzsof6xsvod	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1usKWQ:sdDnJqdCGdPOgcVaTrM3Vy1fL0LrqXfihmpfdHjn2Sk	2025-08-31 12:17:30.425042+00
e48vj1u4sg3jtmht4kft82h20shnrvyg	.eJxVjDsOwyAQBe9CHSFgFwMp0_sMaPkFJxGWjF1FuXtsyUXSvpl5b-ZpW6vfel78lNiVWXb53QLFZ24HSA9q95nHua3LFPih8JN2Ps4pv26n-3dQqde91kRonEMZ0IGCorKNAwgwksAWiDsSGJQQBkWCIdgiqBSpUMuiIQP7fAG3xDau:1usw9H:OPaD18c7LNu8mcWj_HSPev0uto-mzJ8P0CJeQtglfr4	2025-09-02 04:28:07.172705+00
ml2127r30q76ygub9siq9xzf0e52fze4	.eJxVjDsOwjAQBe_iGln-m1DScwZr17vGAeRIcVIh7k4ipYD2zcx7iwTrUtPaeU4jiYvQRpx-R4T85LYTekC7TzJPbZlHlLsiD9rlbSJ-XQ_376BCr1tdwOdSjMlRW4gUUdOAGsyZyTofgynsNqEMwTnGGK32wSMptKgUZhafLytLOOw:1v5yiM:RbMZCTcSH4MDbKk78EQSzfscNvYwPUomIiOzcKencaQ	2025-10-08 03:50:14.421686+00
ebd6v1ef32igzd8qlvsbs69wj7ymhzer	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v3vIV:2W3BGgO5q_k_DiJxQnq6k9nV2d5MHwNPzOA3WJ2rPi4	2025-10-02 11:47:03.598079+00
4ei6ppe0cqs34kg27mwp4h2nb7k9esaa	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1utOEd:KW85c6eNFDZwker9L013GLI-zYD_QewlDtMs32J9Sa4	2025-09-03 10:27:31.1078+00
qfqghy2g907ze4q70o97jf4v922uf0w6	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1utfxV:3Y-DArm9zf2MdM3gUN5IsJQZHJL9Mh5ccoedJBRX82M	2025-09-04 05:23:01.625446+00
ck2rmr30j6typ5l6b3mtx4ria7grtt6o	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1uzXra:dM3etRLxziOaC3vogkLFFRgFEMIMd6N9q67UO7oqjwo	2025-09-20 09:57:10.74822+00
kt96x9hsd2gpap68xxc44276qfworlij	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v1juL:_S0U9BqDyiCqI5j1YW3BmivcxI_kPFkrWNKRivNK8NE	2025-09-26 11:13:05.710164+00
atky830ffborbfwurttsi2cx8aenlhf1	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v1HUV:2R4Z3XfJiNCoqEW7Pw27KDUF4LH22TKh_siuUebt3t8	2025-09-25 04:52:31.537679+00
9flnfrizcldwd98qkbqdommu7nj1cgm3	.eJxVjDsOwjAQBe_iGln-m1DScwZr17vGAeRIcVIh7k4ipYD2zcx7iwTrUtPaeU4jiYvQRpx-R4T85LYTekC7TzJPbZlHlLsiD9rlbSJ-XQ_376BCr1tdwOdSjMlRW4gUUdOAGsyZyTofgynsNqEMwTnGGK32wSMptKgUZhafLytLOOw:1v3YZc:XGnrKkg3tvVALVLmXsc0Y48D3W1qQ7YI38YAQd8CojE	2025-10-01 11:31:12.549343+00
qb3rmjlz5v5pj6pba5fwy67dqf0a5x3b	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v4xgL:Bvmp0iK5qS33GW3VfZWJPjnUZ0wl1NsR1bfv-whw4ww	2025-10-05 08:31:57.586932+00
es8eadbxpw8jeenjgxetlq1p8wae4foh	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v6Q6u:vM0siIPbhsG7cZ2BV8yc7YUSFld5BbssuAEca4pkexQ	2025-10-09 09:05:24.547558+00
vfuz4aca62r0w7ynvatyc37nwo0er1qj	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v79ik:HxZ7xh25tdliLhufg7nlyLVZ3mSyDS7bl6jf22CTGwk	2025-10-11 09:47:30.85971+00
yycf4enmkqk7jbed9yu95ydglnme77zk	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v4wC9:Vom589-ZOXBmzGqirNKAnUwT7-Y5FCuq5LXsqx83ZMI	2025-10-05 06:56:41.688163+00
i32pnyrulxw2o9cpk0mou1h27wnuwkjh	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v9ibX:Isba3o7m508G9wtbYYWWAxvttG5n-sQXs6rH3vnuyzk	2025-10-18 11:26:39.447932+00
us8koywlma14m00e7dm5hylnyjgboq2k	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1vApNv:14_0owtkwFUdUqjweOU5JnpJr4pnZzz5kW3FBMCpVrM	2025-10-21 12:53:11.563362+00
azysr9cxoj85v5v5evwetzwpf9eefh0b	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v7G8G:oY2lOJxWSxOZZRFaBUrGl88omszqRr6_I0OFJZPQkqk	2025-10-11 16:38:16.906732+00
6xqm2p80gldqf7010hvqdo06y7xojm2c	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v5v4I:cMSY5R5BjU8lOUn_wmdpqdI0ak585AF8EJyyR6h8Pm8	2025-10-07 23:56:38.881925+00
2zf79k3a21sko5cn2zsws3ne8h6fsvfc	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1v4Zbd:V4i9pUtQoP4QZOvGMyN6fk45GtvHBBoI16-Dh7wtKec	2025-10-04 06:49:29.906191+00
k0ioljbmdw3nt69ku3eytpwkde85wmr8	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v771w:EaMtrF6LAdqoJ_mVF9sH234ECcO_NxjQ7BC4fXEQK9M	2025-10-11 06:55:08.660011+00
0et0f2zkyily0s57ui3455pvxy4v5ukn	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v6ozU:ntE797FJWl2fWqf-OJZAC0MZWbRQR0cUKYmdVXOMehE	2025-10-10 11:39:24.559129+00
bz85osf06z0yf5074tb3q28qi4fg8qnm	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1v6p5T:eCgO4ppE40Vt7w6ObmJFQYUV_zxUqM4whNijGtmDSbE	2025-10-10 11:45:35.930773+00
tmpykb61iw5j6c8or3sq0nheukreqwds	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v654O:rjVxLmMF01UegvKHGL6EnGtjU3u035W72cnKeVtUaP0	2025-10-08 10:37:24.956559+00
rpn27j4ziy98ppk4cw1b2p72m85vf0jr	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v9GWh:KlQYWPnF17plklrElNRCLjmiqIJs0gT9SB6lIDabc1s	2025-10-17 05:27:47.335052+00
z1khj26fux0jxeqjfqgxlu73e1joqdl2	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v6qns:hKJKjPvBOukPgVLU1dWMMzLZO-uoUjrNT5lzIcMbqXE	2025-10-10 13:35:32.684194+00
bwzch9bbpfqrat4stc0txo18czulb8iv	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v7B5A:kASqO7nxovflwejvhGNWtHa8DQBCRgqOxF2q3EQmcdE	2025-10-11 11:14:44.294286+00
stz7caq5zlattdtie2bwgj6snhh6ida0	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1v7ABJ:NAWcI_kP0CT84NEJf3aHsNcng5d020SJ86wG7xLlF2I	2025-10-11 10:17:01.236281+00
p7ypjo06zgovarwu1bs6horm3dl59pch	.eJxVjsEOgjAQRP-lV6XZbSltOXr35p2UdhGEQEKLHoz_LiRo9DrvzWSerHJLaqsl0lx1gZUMJTv-hrXzPY0bCTc3XifupzHNXc03he808vMUaDjt7t9A62K7tgUWVpDS0qA32ACiRRRKFeRtMEHoJjRgIOQmkJS28bnRXkvvvAR0tVlHk4t9rO4dPWj9k-aFPtngYvoCJkCoDCFDvEBRgihRcRRaWjwAlADs9QbFOE1e:1v7Smn:Vr2nCBX4ARUKUZFNvnx6WPDJxV6n5uciZxcbaueM0-I	2025-10-12 06:08:57.863685+00
r4r59l2af64ds6t2lmmxxatg71vttk1p	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v79gN:9vB_skeFthrv04zxnvPkJyvdovrfFUPtdCgtkyMZoNg	2025-10-11 09:45:03.664005+00
m8qmkfye56tsmjq7heil9xat3fpfdvn5	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v7Tez:8hwVp0a2AFkbOMzS8M4vG6zOUeeChsr3I2ndWuUgIOc	2025-10-12 07:04:57.94437+00
tlfpq10kl2qbrkns9167qlta25g53akt	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v6Q6X:HbW8SqZkqT7ngloIM3Ex1obHuBHVnYfzzqipteM5ggM	2025-10-09 09:05:01.919664+00
qifj49c92enn18zpm6gp55t3nzjher4p	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v7BCP:0Rt2Oz5j0kRz79AY4M8glxsiwl5xocM9nFcOYQLPcCo	2025-10-11 11:22:13.876994+00
wizrpwotp3jcxnppdovv6qq7fq6nceft	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v7VTr:8hWPbvl2OskIEzVAJf7NjP2bPyztqkBlpB1IDW6ZUx0	2025-10-12 09:01:35.284584+00
bfnnii865ebx7f7nmzc6u6pevp4tkxno	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1v7VXb:CrMzUZJJ3dlZntzC9bJ5AhJNWU63H_zh0004f4RFzgY	2025-10-12 09:05:27.842664+00
ai23yow572emcq9mc7o7sbqtw4fq2rwz	.eJxVjDsOwjAQBe_iGln-m1DScwZr17vGAeRIcVIh7k4ipYD2zcx7iwTrUtPaeU4jiYvQRpx-R4T85LYTekC7TzJPbZlHlLsiD9rlbSJ-XQ_376BCr1tdwOdSjMlRW4gUUdOAGsyZyTofgynsNqEMwTnGGK32wSMptKgUZhafLytLOOw:1v6LpQ:QnvTxQxZ3y0He_-E5-_D3v6UypTFORBpFTQ2HP-hYrg	2025-10-09 04:31:04.040626+00
6ak3tr0rsxw3i8cmjm2ovf5wpo5l6iod	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1vAMM0:4yf6S5XahEIsftqJVDz86BKhK_b7SQH1jd6o8_mQpNw	2025-10-20 05:53:16.963828+00
4kkt1spyhgm4m219jentzysq0n5em27a	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1vB6EM:yQ30eWbYj1EohNv35OjnherCQmePF7t-pfRR2YxGjbw	2025-10-22 06:52:26.68676+00
r0qxqnailjb862jnichinkkb5apb1xjl	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v9ghJ:Z6BCKdwy2jbWVwGVvEDrR0XsDcrGtqP-KPpYN4woC74	2025-10-18 09:24:29.473802+00
aeva0ofj1beles97xo450d62cqf78gdw	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1v9ewk:8yol5tIVu85PMFOptqSJSgJmH6ir6AWneUWE6IMS4UY	2025-10-18 07:32:18.033732+00
o5sgxiyu421o00l1t526pcwbgl1hw27x	.eJxVjDsOwjAQBe_iGln-m1DScwZr17vGAeRIcVIh7k4ipYD2zcx7iwTrUtPaeU4jiYvQRpx-R4T85LYTekC7TzJPbZlHlLsiD9rlbSJ-XQ_376BCr1tdwOdSjMlRW4gUUdOAGsyZyTofgynsNqEMwTnGGK32wSMptKgUZhafLytLOOw:1vBQuv:KbgZqlhCphrNUmZYx9gHmkbr3aUyRZz1_f3c5w4v1pw	2025-10-23 04:57:45.373154+00
v5hmvepbbfez77fly4n4b0jsel6w3hmw	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1vArfm:JHo3Pj_ReD5E7zgD-kg-MKvbmEg83YYniWtJsqLBfr0	2025-10-21 15:19:46.943409+00
niozqigjgy3pn41bjtqqs8dcm32etd9x	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1vBUiz:I8o51q5GXMCNu_AJZqrEB0HUqAgi89WRUyPbLZoTn5E	2025-10-23 09:01:41.119625+00
za9blh6eu5e3oq6k7yjj6fagh4cqfm4o	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1vBUkW:pMtGE91ywqNweXKFaUWE7hZ00bQyiYTTADR7o5bmUUc	2025-10-23 09:03:16.898327+00
g2z82j7qnf3kpm9eh4s2ys4fc7rj1u0q	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1vBmma:1IQXhaO2NnwFNT-LCvFtpF-K-H7KgZO8EjTp2iznPy0	2025-10-24 04:18:36.508117+00
jo7cydkg2iqs4gxspb81b8ul45xr5pyf	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1vA2z8:nEPkUO6pcH9AA_pyNVfkuNv76tsZKvusg3umMYWMp8w	2025-10-19 09:12:22.174978+00
7qz1qy5lm5xbh1up7lfb3nt6eron1vqs	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1v8cdR:cTP2YqcRYz2eNajNNLJQywORCa8WBAOMC8NAcwJDJYI	2025-10-15 10:52:05.728807+00
n7pdp4lhzi80t2wta9a7kootdmiostat	.eJxVjMsKwyAQAP_FcxHXV7DH3vsNsupuTVsMxOQU-u9FyKG9zgxziIj7VuPeaY1zEVehxeWXJcwvakOUJ7bHIvPStnVOciTytF3el0Lv29n-DSr2OrYADoJjS-y8VhMabRwpYFWcsWAAWTOgScFbpdhYzM4CeZyIQ8hWfL6wrzb5:1v8cf9:FjpIH4nnN6_bO5gRBUsrmX4XfhZxLJU5XCGOyptD03M	2025-10-15 10:53:51.061557+00
rg6pgmcjkhuojnurrvg1jqpu5xy87d35	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1vBn7i:IpqwQaZ2DAHwJm5rfDtace8lw8xxO0-Q9wUfnvBAaqY	2025-10-24 04:40:26.911561+00
qwy1z7fa9l2gizmf1v5dr5fn3ykluxlg	.eJxVjDsOwjAQBe_iGln-m1DScwZr17vGAeRIcVIh7k4ipYD2zcx7iwTrUtPaeU4jiYvQRpx-R4T85LYTekC7TzJPbZlHlLsiD9rlbSJ-XQ_376BCr1tdwOdSjMlRW4gUUdOAGsyZyTofgynsNqEMwTnGGK32wSMptKgUZhafLytLOOw:1vBQ6y:7NnyfpeIc34Jb2atudZUbqwL1hDql7PO_WMxt_rIvIY	2025-10-23 04:06:08.626481+00
oxmvfhxy8nztv43fgxhbw26mhsxx90wz	.eJxVjEEOwiAQRe_C2hAGShlcuvcMBGZAqoYmpV0Z765NutDtf-_9lwhxW2vYel7CxOIswIjT75giPXLbCd9ju82S5rYuU5K7Ig_a5XXm_Lwc7t9Bjb1-aw2j19k6g0AIRQF4AG3tmMkzsnaFi0LFA3I2xhca0JEzFMkoiAnF-wPZ_zd7:1vBQB1:UHg_cYiSaZ6zeiio03nZYLKHGVtwKEYuzETA-3tSAvs	2025-10-23 04:10:19.29924+00
fv6qxib93ms7r3n8uuxde0qxtw9js7uf	.eJxVjDsOwjAQBe_iGlleY2c3lPQ5g7X-4QCypTipEHeHSCmgfTPzXsLxtha39bS4OYqLsOL0u3kOj1R3EO9cb02GVtdl9nJX5EG7nFpMz-vh_h0U7uVbD3bMqEfPhMYwEORMPhEqQuujgcQqDJDxHBRp8ipitmARQFtGyEa8P9IzNyE:1vBQYI:eubQk8F3nxHoXEgGGcnx7VfTHnaxUG7HYIQNciQmTNM	2025-10-23 04:34:22.763638+00
uboqxjpc0xl66gkjrposiq366qt2lo1m	.eJxVjEEOwiAQAP_C2RBAYMGjd99AdlkqVUOT0p6MfzckPeh1ZjJvkXDfatp7WdPM4iJAnH4ZYX6WNgQ_sN0XmZe2rTPJkcjDdnlbuLyuR_s3qNjr2BYygXUAp8GyJUtIJWsM2jil4GxU8NF6Rp_ZaTexs6CmGIuFGCIE8fkC0pI3Ag:1vB6Bs:4FH3BwEJLGBF1MS9-5sy8CjiUvV9bxaEuKOjn5nqmLk	2025-10-22 06:49:52.722881+00
\.


--
-- Data for Name: hob_hobsetting; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hob_hobsetting (id, dashboard_layout, notification_preferences, user_id) FROM stdin;
\.


--
-- Data for Name: leads_lead; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.leads_lead (id, name, phone, email, priority, location, source, custom_source, created_at, updated_at, assigned_to_id, program, status, assigned_date, document_status, documents_received, processing_executive_id, processing_notes, processing_status, processing_status_date, registration_date, remarks) FROM stdin;
10	Not Aquired	+91 73065 74107		MEDIUM		WHATSAPP		2025-08-06 06:17:11.821594+00	2025-08-18 05:26:38.810596+00	5	\N	ENQUIRY	2025-08-18 05:26:38.807857+00	PENDING		\N		PENDING	2025-08-06 06:17:11.82157+00	\N	\N
231	Akhil S	7510152045		MEDIUM		INSTAGRAM	\N	2025-10-01 03:51:24.039496+00	2025-10-03 06:23:32.676306+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-01 03:51:24.039471+00	\N	
54	Not Acquired	+91 97450 39407		MEDIUM		WHATSAPP		2025-08-06 07:13:37.263418+00	2025-08-18 05:25:03.265637+00	11	\N	ENQUIRY	2025-08-18 05:25:03.261609+00	PENDING		\N		PENDING	2025-08-06 07:13:37.26339+00	\N	\N
9	Not Aquired	+91 87143 90809		MEDIUM		WHATSAPP		2025-08-06 06:16:32.54098+00	2025-08-18 05:26:41.089397+00	5	\N	ENQUIRY	2025-08-18 05:26:41.08711+00	PENDING		\N		PENDING	2025-08-06 06:16:32.540956+00	\N	\N
8	Not Aquired	+91 80058 76903		MEDIUM		WHATSAPP		2025-08-06 06:15:36.586899+00	2025-08-18 05:26:42.724009+00	5	MASTERS	ENQUIRY	2025-08-18 05:26:42.721521+00	PENDING		\N		PENDING	2025-08-06 06:15:36.586876+00	\N	\N
7	Not aquired	+91 91007 91778		MEDIUM		WHATSAPP		2025-08-06 06:13:27.760582+00	2025-08-18 05:26:44.838415+00	5	MASTERS	ENQUIRY	2025-08-18 05:26:44.835387+00	PENDING		\N		PENDING	2025-08-06 06:13:27.760557+00	\N	\N
53	Not Acquired	+91 89438 87857		MEDIUM		WHATSAPP		2025-08-06 07:05:05.165894+00	2025-08-18 05:25:04.774117+00	11	\N	ENQUIRY	2025-08-18 05:25:04.770453+00	PENDING		\N		PENDING	2025-08-06 07:05:05.165867+00	\N	\N
6	MUHAMMED SAMEED	+91 70343 35901		MEDIUM	Malappuram	WHATSAPP		2025-08-06 06:10:33.669241+00	2025-08-18 05:26:46.220072+00	5	\N	ENQUIRY	2025-08-18 05:26:46.217259+00	PENDING		\N		PENDING	2025-08-06 06:10:33.669216+00	2025-08-06 06:20:20.750064+00	\N
5	ANANDHAKRISHNAN	+91 79948 19506		MEDIUM	Kollam	WHATSAPP		2025-08-06 06:09:08.267367+00	2025-08-18 05:26:48.081082+00	5	\N	ENQUIRY	2025-08-18 05:26:48.077073+00	PENDING		\N		PENDING	2025-08-06 06:09:08.267343+00	\N	\N
4	Iraaz	+91 78893 75071		MEDIUM		WHATSAPP		2025-08-06 06:07:15.076258+00	2025-08-18 05:26:50.265918+00	5	\N	ENQUIRY	2025-08-18 05:26:50.263231+00	PENDING		\N		PENDING	2025-08-06 06:07:15.076233+00	\N	\N
3	Rosemol	+91 80890 81377		MEDIUM		WHATSAPP		2025-08-06 06:06:05.082712+00	2025-08-18 05:26:51.545007+00	5	\N	ENQUIRY	2025-08-18 05:26:51.542453+00	PENDING		\N		PENDING	2025-08-06 06:06:05.082687+00	\N	\N
2	ASHIQ	+91 97475 32273		MEDIUM		WHATSAPP		2025-08-06 06:04:58.855511+00	2025-08-18 05:26:53.842808+00	5	\N	ENQUIRY	2025-08-18 05:26:53.83854+00	PENDING		\N		PENDING	2025-08-06 06:04:58.855483+00	\N	\N
13	Not Aquired	+91 85903 62187		MEDIUM		WHATSAPP		2025-08-06 06:19:49.565119+00	2025-08-18 05:27:01.176104+00	5	GCC	ENQUIRY	2025-08-18 05:26:28.145758+00	PENDING		\N		PENDING	2025-08-06 06:19:49.565094+00	\N	\N
14	Not Aquired	+91 6238 393 06		MEDIUM		WHATSAPP		2025-08-06 06:20:39.786774+00	2025-08-18 05:27:03.18927+00	5	\N	ENQUIRY	2025-08-18 05:26:25.027433+00	PENDING		\N		PENDING	2025-08-06 06:20:39.78675+00	\N	\N
15	Not Aquired	+91 98466 97589		MEDIUM		WHATSAPP		2025-08-06 06:21:31.807969+00	2025-08-18 05:27:05.523478+00	5	\N	ENQUIRY	2025-08-18 05:26:23.568091+00	PENDING		\N		PENDING	2025-08-06 06:21:31.807944+00	\N	\N
17	PRADEEP	+91 6380 181 96		MEDIUM	Tamilnadu	WHATSAPP		2025-08-06 06:24:57.214872+00	2025-08-18 06:15:36.336271+00	8	\N	ENQUIRY	2025-08-18 06:15:36.333069+00	PENDING		\N		PENDING	2025-08-06 06:24:57.214843+00	\N	\N
18	athul	+91 90747 37881		MEDIUM		WHATSAPP		2025-08-06 06:26:21.017465+00	2025-08-19 08:10:29.923999+00	8	GCC	ENQUIRY	2025-08-18 06:15:36.68974+00	PENDING		\N		PENDING	2025-08-06 06:26:21.01744+00	\N	Interested 
24	Not Aquired	+91 82813 25745		MEDIUM		WHATSAPP		2025-08-06 06:32:46.039546+00	2025-08-22 05:17:46.744036+00	8	\N	ENQUIRY	2025-08-22 05:17:46.741253+00	PENDING		\N		PENDING	2025-08-06 06:32:46.039523+00	\N	\N
21	MEBIN	+91 90611 47721		MEDIUM		WHATSAPP		2025-08-06 06:28:58.400707+00	2025-08-18 11:09:36.694826+00	8	\N	ENQUIRY	2025-08-18 06:15:43.700324+00	PENDING		\N		PENDING	2025-08-06 06:28:58.400683+00	\N	Incoming calls are not allow
23	IRFAN	+91 95739 31617		MEDIUM		WHATSAPP		2025-08-06 06:31:57.623897+00	2025-08-18 09:13:47.085113+00	8	\N	ENQUIRY	2025-08-18 06:15:53.398601+00	PENDING		\N		PENDING	2025-08-06 06:31:57.623872+00	\N	NAC
22	SACHU	+91 75939 39823		MEDIUM		WHATSAPP		2025-08-06 06:31:05.920093+00	2025-08-18 11:10:09.491121+00	8	\N	ENQUIRY	2025-08-18 06:15:46.625862+00	PENDING		\N		PENDING	2025-08-06 06:31:05.920066+00	\N	           NAC       
28	Harisankar	+91 96452 55799		MEDIUM		WHATSAPP		2025-08-06 06:36:46.411928+00	2025-08-18 06:23:51.824206+00	8	\N	ENQUIRY	2025-08-18 06:16:05.136296+00	PENDING		\N		PENDING	2025-08-06 06:36:46.411904+00	\N	incoming calls are not allowed
195	Not Acquired	9846596589	\N	MEDIUM	\N	WHATSAPP	\N	2025-08-28 08:34:20.879452+00	2025-08-28 08:34:20.879458+00	\N	\N	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-08-28 08:34:20.879426+00	\N	\N
29	DIYA	+91 77366 25769		MEDIUM		WHATSAPP		2025-08-06 06:37:23.393793+00	2025-08-22 09:13:51.047745+00	8	\N	ENQUIRY	2025-08-22 05:17:53.959597+00	PENDING		\N		PENDING	2025-08-06 06:37:23.393744+00	\N	NAC  
30	Not Aquired	6289 379 487		MEDIUM		WHATSAPP		2025-08-06 06:38:18.233664+00	2025-08-22 05:17:55.718404+00	8	\N	ENQUIRY	2025-08-22 05:17:55.714368+00	PENDING		\N		PENDING	2025-08-06 06:38:18.233638+00	\N	\N
188	Not Acquired	9526703874	\N	MEDIUM	\N	WHATSAPP	\N	2025-08-27 04:45:41.413734+00	2025-08-27 04:45:41.413739+00	\N	\N	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-08-27 04:45:41.413704+00	\N	\N
25	Not Aquired	+91 90374 14170		MEDIUM		WHATSAPP		2025-08-06 06:33:20.784436+00	2025-08-27 09:45:29.797124+00	8	\N	ENQUIRY	2025-08-22 05:17:47.527818+00	PENDING		\N		PENDING	2025-08-06 06:33:20.784409+00	\N	NAC
194	Not Acquired	8714700399	\N	MEDIUM	\N	WHATSAPP	\N	2025-08-27 11:21:37.496888+00	2025-08-27 11:21:37.496893+00	\N	\N	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-08-27 11:21:37.496862+00	\N	\N
52	Not Acquired	+91 91236 51263		MEDIUM		WHATSAPP		2025-08-06 07:04:07.937967+00	2025-08-18 05:25:06.769482+00	11	\N	ENQUIRY	2025-08-18 05:25:06.766139+00	PENDING		\N		PENDING	2025-08-06 07:04:07.937942+00	\N	\N
50	SHAMIL	+91 90616 52940		MEDIUM		WHATSAPP		2025-08-06 07:02:49.914183+00	2025-08-18 05:25:10.756879+00	11	\N	ENQUIRY	2025-08-18 05:25:10.753968+00	PENDING		\N		PENDING	2025-08-06 07:02:49.914158+00	\N	\N
49	ADBIN VARGHESE	+91 90485 82311		MEDIUM	Koratty, Thrissur	WHATSAPP		2025-08-06 07:01:51.681878+00	2025-08-18 05:25:12.35379+00	11	\N	ENQUIRY	2025-08-18 05:25:12.350918+00	PENDING		\N		PENDING	2025-08-06 07:01:51.681852+00	\N	\N
48	ADITHYAN	+91 95396 43651		MEDIUM		WHATSAPP		2025-08-06 07:00:44.543927+00	2025-08-18 05:25:14.163498+00	11	\N	ENQUIRY	2025-08-18 05:25:14.1597+00	PENDING		\N		PENDING	2025-08-06 07:00:44.543897+00	\N	\N
47	JEFFIN	+91 79072 68845		MEDIUM		WHATSAPP		2025-08-06 06:59:45.868866+00	2025-08-18 05:25:15.470784+00	11	\N	ENQUIRY	2025-08-18 05:25:15.468114+00	PENDING		\N		PENDING	2025-08-06 06:59:45.868842+00	\N	\N
46	Not Acquired	+91 79072 68845		MEDIUM		WHATSAPP		2025-08-06 06:59:09.563922+00	2025-08-18 05:25:17.642802+00	11	\N	ENQUIRY	2025-08-18 05:25:17.64049+00	PENDING		\N		PENDING	2025-08-06 06:59:09.563895+00	\N	\N
45	Not Acquired	+91 99476 69512		MEDIUM		WHATSAPP		2025-08-06 06:53:43.57919+00	2025-08-18 05:25:19.314359+00	11	\N	ENQUIRY	2025-08-18 05:25:19.310712+00	PENDING		\N		PENDING	2025-08-06 06:53:43.579164+00	\N	\N
44	Not Acquired	+919947969821		MEDIUM		WHATSAPP		2025-08-06 06:53:12.649923+00	2025-08-18 05:25:20.714599+00	11	\N	ENQUIRY	2025-08-18 05:25:20.712096+00	PENDING		\N		PENDING	2025-08-06 06:53:12.649897+00	\N	\N
42	Not Acquired	+91 94965 78281		MEDIUM		WHATSAPP		2025-08-06 06:51:42.433649+00	2025-08-18 05:25:24.029022+00	11	\N	ENQUIRY	2025-08-18 05:25:24.025233+00	PENDING		\N		PENDING	2025-08-06 06:51:42.433623+00	\N	\N
41	Not Acquired	+91 75108 94634		MEDIUM		WHATSAPP		2025-08-06 06:51:10.812617+00	2025-08-18 05:25:25.427899+00	11	\N	ENQUIRY	2025-08-18 05:25:25.425299+00	PENDING		\N		PENDING	2025-08-06 06:51:10.812592+00	\N	\N
40	ATHUL P	+91 90619 56455		MEDIUM	Nilambur	WHATSAPP		2025-08-06 06:49:52.83254+00	2025-08-18 05:25:29.220137+00	11	MASTERS	ENQUIRY	2025-08-18 05:25:29.217654+00	PENDING		\N		PENDING	2025-08-06 06:49:52.832514+00	\N	\N
39	Not Aquired	918015480093		MEDIUM		WHATSAPP		2025-08-06 06:47:32.644202+00	2025-08-18 05:25:30.553948+00	11	\N	ENQUIRY	2025-08-18 05:25:30.550421+00	PENDING		\N		PENDING	2025-08-06 06:47:32.644176+00	\N	\N
38	siva	+91 6300 041 57		MEDIUM		WHATSAPP		2025-08-06 06:46:36.771611+00	2025-08-18 05:25:32.442222+00	11	\N	ENQUIRY	2025-08-18 05:25:32.43813+00	PENDING		\N		PENDING	2025-08-06 06:46:36.771587+00	\N	\N
37	Muhammed Adil Kp	+91 75580 99848		MEDIUM	Koppam	WHATSAPP		2025-08-06 06:45:56.486458+00	2025-08-18 05:25:35.020533+00	11	\N	ENQUIRY	2025-08-18 05:25:35.017995+00	PENDING		\N		PENDING	2025-08-06 06:45:56.486433+00	\N	\N
36	AMEYA ASHA	+91 95443 10090		MEDIUM		WHATSAPP		2025-08-06 06:43:54.969041+00	2025-08-18 05:25:36.34939+00	11	MASTERS	ENQUIRY	2025-08-18 05:25:36.346524+00	PENDING		\N		PENDING	2025-08-06 06:43:54.969016+00	\N	\N
34	ANITA SUDHAKRAN	+91 79078 85044		MEDIUM		WHATSAPP		2025-08-06 06:41:44.260946+00	2025-08-18 05:25:41.6964+00	11	\N	ENQUIRY	2025-08-18 05:25:41.693903+00	PENDING		\N		PENDING	2025-08-06 06:41:44.26092+00	\N	\N
33	GOPI	+91 87601 03523		MEDIUM		WHATSAPP		2025-08-06 06:40:51.48635+00	2025-08-18 05:25:43.072466+00	11	\N	ENQUIRY	2025-08-18 05:25:43.069027+00	PENDING		\N		PENDING	2025-08-06 06:40:51.486324+00	\N	\N
32	Not Aquired	+91 70778 35549		MEDIUM		WHATSAPP		2025-08-06 06:39:49.286752+00	2025-08-18 05:25:45.481649+00	11	\N	ENQUIRY	2025-08-18 05:25:45.477961+00	PENDING		\N		PENDING	2025-08-06 06:39:49.286728+00	\N	\N
31	Not Aquired	+91 97685 70655		MEDIUM		WHATSAPP		2025-08-06 06:38:56.230308+00	2025-08-18 05:25:47.315936+00	11	\N	ENQUIRY	2025-08-18 05:25:47.313242+00	PENDING		\N		PENDING	2025-08-06 06:38:56.230283+00	\N	\N
12	Not Aquired	+91 90805 88382		MEDIUM		WHATSAPP		2025-08-06 06:19:11.041229+00	2025-08-18 05:26:59.199419+00	5	\N	ENQUIRY	2025-08-18 05:26:30.550406+00	PENDING		\N		PENDING	2025-08-06 06:19:11.041204+00	\N	\N
112	Not Acquired	+91 79943 66270		MEDIUM		WHATSAPP		2025-08-07 09:54:47.85134+00	2025-08-18 10:23:38.479438+00	5	\N	ENQUIRY	2025-08-11 05:50:49.276994+00	PENDING		\N		PENDING	2025-08-07 09:54:47.851313+00	\N	busy call back
111	Jering	+91 79072 82016		MEDIUM		WHATSAPP		2025-08-07 09:54:15.089103+00	2025-08-18 10:24:13.578396+00	5	\N	ENQUIRY	2025-08-11 05:50:50.378209+00	PENDING		\N		PENDING	2025-08-07 09:54:15.089077+00	\N	NAC
77	BHARATH	+91 81579 87239		MEDIUM		WHATSAPP		2025-08-06 07:29:16.121997+00	2025-08-22 05:17:58.79466+00	8	Ausbildung	ENQUIRY	2025-08-22 05:17:58.792031+00	PENDING		\N		PENDING	2025-08-06 07:29:16.121971+00	\N	B2 full module,Nursing
78	Not Acquired	+91 90969 79642		MEDIUM		WHATSAPP		2025-08-06 07:29:46.901149+00	2025-08-22 05:18:00.0105+00	8	\N	ENQUIRY	2025-08-22 05:18:00.006977+00	PENDING		\N		PENDING	2025-08-06 07:29:46.901125+00	\N	\N
60	VIMAL TOMAS	+91 92072 12704		MEDIUM		WHATSAPP		2025-08-06 07:16:43.252959+00	2025-08-18 05:24:51.427174+00	11	\N	ENQUIRY	2025-08-18 05:24:51.4234+00	PENDING		\N		PENDING	2025-08-06 07:16:43.252934+00	\N	\N
73	PRITHVI RAJ	+91 82398 52224		MEDIUM		WHATSAPP		2025-08-06 07:25:53.138509+00	2025-08-14 09:25:48.772219+00	8	\N	ENQUIRY	2025-08-12 10:57:27.622085+00	PENDING		\N		PENDING	2025-08-06 07:25:53.138485+00	\N	B2B
76	Thomas	+91 70251 21375		MEDIUM		WHATSAPP		2025-08-06 07:28:41.914013+00	2025-08-14 09:17:36.697294+00	8	German job	ENQUIRY	2025-08-12 11:02:16.860097+00	PENDING		\N		PENDING	2025-08-06 07:28:41.913988+00	\N	NAC
75	NIVIN JOY	+91 96645 04867		MEDIUM	Thrissur	WHATSAPP		2025-08-06 07:27:52.618187+00	2025-08-14 09:23:57.672965+00	8	Ausbuildung	ENQUIRY	2025-08-12 11:02:15.384011+00	PENDING		\N		PENDING	2025-08-06 07:27:52.618162+00	\N	for aus -b1-3module 
74	NIVIN JOY	+91 96645 04867		MEDIUM	Thrissur	WHATSAPP		2025-08-06 07:27:52.54584+00	2025-08-14 09:15:46.084989+00	8	Ausbuildung	ENQUIRY	2025-08-12 10:56:28.490821+00	PENDING		\N		PENDING	2025-08-06 07:27:52.545816+00	\N	\N
72	Not Acquired	+91 97479 66962		MEDIUM		WHATSAPP		2025-08-06 07:25:14.43199+00	2025-08-14 09:37:18.588284+00	8	\N	ENQUIRY	2025-08-12 10:57:29.180362+00	PENDING		\N		PENDING	2025-08-06 07:25:14.431966+00	\N	NAC
69	VISHNU P	+91 80862 38607		MEDIUM		WHATSAPP		2025-08-06 07:23:10.829766+00	2025-08-14 09:47:57.268952+00	8	\N	ENQUIRY	2025-08-12 10:57:34.869376+00	PENDING		\N		PENDING	2025-08-06 07:23:10.829741+00	\N	NAC
71	Not Acquired	+91 79948 24836		MEDIUM		WHATSAPP		2025-08-06 07:24:39.159278+00	2025-08-14 09:42:50.740943+00	8	PVP/AUSBILDUNG	ENQUIRY	2025-08-12 10:57:30.485479+00	PENDING		\N		PENDING	2025-08-06 07:24:39.159255+00	\N	interested
70	Fidha faisal	+91 95620 41859		MEDIUM		WHATSAPP		2025-08-06 07:24:01.424739+00	2025-08-14 09:46:26.43476+00	8	Ausbildung	ENQUIRY	2025-08-12 10:57:33.370604+00	PENDING		\N		PENDING	2025-08-06 07:24:01.424715+00	\N	Physiotherapy
67	Not Acquired	+91 79049 22644		MEDIUM		WHATSAPP		2025-08-06 07:22:04.457853+00	2025-08-14 09:56:51.557867+00	8	\N	ENQUIRY	2025-08-12 10:57:38.842721+00	PENDING		\N		PENDING	2025-08-06 07:22:04.457827+00	\N	NAC
66	Not Acquired	+91 6282 775714		MEDIUM		WHATSAPP		2025-08-06 07:21:04.980181+00	2025-08-14 10:17:58.755979+00	8	\N	ENQUIRY	2025-08-12 10:57:40.836562+00	PENDING		\N		PENDING	2025-08-06 07:21:04.980009+00	\N	NAC 
79	Alexander k mathai	+91 90729 15122		MEDIUM	Kottayam	WHATSAPP		2025-08-06 07:31:23.593159+00	2025-08-22 05:18:02.179265+00	8	\N	ENQUIRY	2025-08-22 05:18:02.176588+00	PENDING		\N		PENDING	2025-08-06 07:31:23.593132+00	\N	\N
64	ATHULYA	+91 75930 45486		MEDIUM		WHATSAPP		2025-08-06 07:19:39.51103+00	2025-08-14 10:51:36.633931+00	8	\N	ENQUIRY	2025-08-12 11:02:10.448995+00	PENDING		\N		PENDING	2025-08-06 07:19:39.511006+00	\N	       NAC
104	Akshay	+91 80751 22368		MEDIUM		WHATSAPP		2025-08-07 04:27:28.659423+00	2025-08-16 04:32:42.585833+00	6	German Language	ENQUIRY	2025-08-11 05:56:37.608311+00	PENDING		\N		PENDING	2025-08-07 04:27:28.659379+00	\N	not available
103	Not Acquired	+91 97471 94078		MEDIUM		WHATSAPP		2025-08-07 04:25:57.865806+00	2025-08-16 04:38:45.422894+00	6	\N	ENQUIRY	2025-08-11 05:56:39.598584+00	PENDING		\N		PENDING	2025-08-07 04:25:57.865779+00	\N	not enqury
102	Aswini	+91 96333 50225		MEDIUM	Trivandrum	WHATSAPP		2025-08-07 04:24:20.451021+00	2025-08-16 04:40:28.126091+00	6	German Language	ENQUIRY	2025-08-11 05:56:41.371707+00	PENDING		\N		PENDING	2025-08-07 04:24:20.450995+00	\N	not available
100	Sharon	+91 70124 05540		MEDIUM		WHATSAPP		2025-08-07 04:21:20.854903+00	2025-09-30 11:30:11.098739+00	12	Masters	ENQUIRY	2025-08-11 05:56:44.722982+00	PENDING		\N		PENDING	2025-08-07 04:21:20.854876+00	\N	not available
97	Not Acquired	+91 6235 863429		MEDIUM		WHATSAPP		2025-08-07 04:19:06.407144+00	2025-09-30 11:30:19.348574+00	12	\N	ENQUIRY	2025-08-11 05:56:49.59983+00	PENDING		\N		PENDING	2025-08-07 04:19:06.407119+00	\N	not available
96	Not Acquired	+91 83093 46805		MEDIUM		WHATSAPP		2025-08-07 04:18:09.896339+00	2025-09-30 11:30:21.714642+00	12	\N	ENQUIRY	2025-08-11 05:56:51.336885+00	PENDING		\N		PENDING	2025-08-07 04:18:09.896307+00	\N	not available
95	Not Acquired	+91 83093 46805		MEDIUM		WHATSAPP		2025-08-07 04:18:09.677815+00	2025-09-30 11:30:23.492464+00	12	\N	ENQUIRY	2025-08-11 05:56:53.257721+00	PENDING		\N		PENDING	2025-08-07 04:18:09.677783+00	\N	repeated no
89	Not Acquired	+91 75108 25741		MEDIUM		WHATSAPP		2025-08-06 07:43:28.03789+00	2025-09-30 11:30:29.28683+00	12	Jobs	ENQUIRY	2025-08-11 05:56:56.065783+00	PENDING		\N		PENDING	2025-08-06 07:43:28.03786+00	\N	share detials
88	Not Acquired	+91 86063 55646		MEDIUM		WHATSAPP		2025-08-06 07:38:38.421434+00	2025-09-30 11:30:34.511248+00	12	Not sure	ENQUIRY	2025-08-11 05:56:57.805672+00	PENDING		\N		PENDING	2025-08-06 07:38:38.421409+00	\N	prefferd uk already join another consultancy
233	Aleena Mary Mathew	8075661415		MEDIUM		INSTAGRAM	\N	2025-10-01 03:56:40.473302+00	2025-10-03 06:23:08.839363+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-01 03:56:40.473278+00	\N	
63	Not Acquired	+91 99473 00652		MEDIUM		WHATSAPP		2025-08-06 07:19:06.899261+00	2025-08-22 05:52:23.196275+00	8	\N	ENQUIRY	2025-08-12 11:02:08.608465+00	PENDING		\N		PENDING	2025-08-06 07:19:06.899237+00	\N	NAC
87	Mujeeb	+966 50 1480638		MEDIUM		WHATSAPP		2025-08-06 07:38:03.605679+00	2025-09-30 11:30:36.621582+00	12	Not sure	ENQUIRY	2025-08-11 05:56:58.902181+00	PENDING		\N		PENDING	2025-08-06 07:38:03.605653+00	\N	\N
84	Not Acquired	+7 995 386-42-6		MEDIUM		WHATSAPP		2025-08-06 07:35:31.572753+00	2025-09-30 11:30:43.001788+00	12	Medical PG	ENQUIRY	2025-08-11 05:57:03.498599+00	PENDING		\N		PENDING	2025-08-06 07:35:31.572728+00	\N	\N
82	shebi	+91 96455 43371		MEDIUM		WHATSAPP		2025-08-06 07:33:07.781798+00	2025-09-30 11:30:47.669172+00	12	\N	ENQUIRY	2025-08-11 05:57:06.487756+00	PENDING		\N		PENDING	2025-08-06 07:33:07.781773+00	\N	not available
59	JOSHNA	+91 76679 31676		MEDIUM		WHATSAPP		2025-08-06 07:16:10.676061+00	2025-08-18 05:24:54.275401+00	11	\N	ENQUIRY	2025-08-18 05:24:54.272795+00	PENDING		\N		PENDING	2025-08-06 07:16:10.676035+00	\N	\N
58	Not Acquired	+91 74079 32834		MEDIUM		WHATSAPP		2025-08-06 07:15:43.52726+00	2025-08-18 05:24:55.785982+00	11	\N	ENQUIRY	2025-08-18 05:24:55.783547+00	PENDING		\N		PENDING	2025-08-06 07:15:43.527235+00	\N	\N
57	Not Acquired	+91 88482 75237		MEDIUM		WHATSAPP		2025-08-06 07:15:16.421106+00	2025-08-18 05:24:58.090212+00	11	\N	ENQUIRY	2025-08-18 05:24:58.087771+00	PENDING		\N		PENDING	2025-08-06 07:15:16.421082+00	\N	\N
56	Not Acquired	+91 75618 55650		MEDIUM		WHATSAPP		2025-08-06 07:14:42.977037+00	2025-08-18 05:24:59.648718+00	11	\N	ENQUIRY	2025-08-18 05:24:59.645235+00	PENDING		\N		PENDING	2025-08-06 07:14:42.977012+00	\N	\N
55	JENY ASNA	+91 96330 04872		MEDIUM		WHATSAPP		2025-08-06 07:14:09.796014+00	2025-08-18 05:25:01.109971+00	11	\N	ENQUIRY	2025-08-18 05:25:01.1072+00	PENDING		\N		PENDING	2025-08-06 07:14:09.79599+00	\N	\N
107	Not Acquired	+91 98468 08732		MEDIUM		WHATSAPP		2025-08-07 04:29:26.604813+00	2025-09-03 06:00:45.331516+00	5	None	ENQUIRY	2025-08-11 05:50:53.389461+00	PENDING		\N		PENDING	2025-08-07 04:29:26.604784+00	\N	NAC
62	Not Acquired	+91 97783 64338		MEDIUM		WHATSAPP		2025-08-06 07:18:28.676239+00	2025-08-22 05:57:21.458435+00	8	gcc	ENQUIRY	2025-08-12 11:02:07.141689+00	PENDING		\N		PENDING	2025-08-06 07:18:28.676216+00	\N	Details share
106	Meenu	+91 98463 06264		MEDIUM		WHATSAPP		2025-08-07 04:28:59.319496+00	2025-09-03 06:01:56.070997+00	5	\N	ENQUIRY	2025-08-11 05:50:54.778664+00	PENDING		\N		PENDING	2025-08-07 04:28:59.31947+00	\N	NAC
101	Ameena Ajeeb	+91 85904 83391		MEDIUM		WHATSAPP		2025-08-07 04:21:53.704733+00	2025-09-30 11:30:08.537499+00	12	\N	ENQUIRY	2025-08-11 05:56:42.99728+00	PENDING		\N		PENDING	2025-08-07 04:21:53.704706+00	\N	cut the call 
86	Not Acquired	+91 94368 02775		MEDIUM		WHATSAPP		2025-08-06 07:37:07.933757+00	2025-09-30 11:30:38.308968+00	12	MBBS	ENQUIRY	2025-08-11 05:57:00.485355+00	PENDING		\N		PENDING	2025-08-06 07:37:07.933732+00	\N	not interested
83	Not Acquired	+91 94191 53301		MEDIUM		WHATSAPP		2025-08-06 07:34:16.777114+00	2025-09-30 11:30:45.048903+00	12	\N	ENQUIRY	2025-08-11 05:57:05.400909+00	PENDING		\N		PENDING	2025-08-06 07:34:16.777089+00	\N	share detials
124	Not Acquired	+91 95929 40398		MEDIUM		WHATSAPP		2025-08-07 10:30:18.358463+00	2025-08-18 05:38:32.208316+00	5	Ausbildung	INTERESTED	2025-08-11 05:50:27.150439+00	PENDING		\N		PENDING	2025-08-07 10:30:18.358443+00	\N	looking for ausbildung in germany,our full details shared in whtsapp
115	Not Acquired	+91 92077 87023		MEDIUM		WHATSAPP		2025-08-07 09:55:59.995776+00	2025-08-18 10:19:15.194229+00	5	\N	ENQUIRY	2025-08-11 05:50:43.710217+00	PENDING		\N		PENDING	2025-08-07 09:55:59.99575+00	\N	NAC
123	Not Acquired	+91 95264 08410		MEDIUM		WHATSAPP		2025-08-07 10:29:40.466433+00	2025-08-18 09:14:54.811332+00	5	\N	ENQUIRY	2025-08-11 05:50:28.54444+00	PENDING		\N		PENDING	2025-08-07 10:29:40.466412+00	\N	NAC
160	Not Acquired	9064881334		MEDIUM		WHATSAPP		2025-08-08 06:10:38.649317+00	2025-08-14 10:55:56.87377+00	9	GCC	ENQUIRY	2025-08-11 05:46:10.874572+00	PENDING		\N		PENDING	2025-08-08 06:10:38.649293+00	\N	Details Shared
162	Not Acquired	9846141581		MEDIUM		WHATSAPP		2025-08-08 06:12:24.827894+00	2025-08-14 09:48:56.913992+00	9	\N	ENQUIRY	2025-08-11 05:46:07.108669+00	PENDING		\N		PENDING	2025-08-08 06:12:24.827869+00	\N	Send message
161	Not Acquired	7736876194		MEDIUM		WHATSAPP		2025-08-08 06:11:47.365354+00	2025-08-14 10:49:06.926233+00	9	German langauge	ENQUIRY	2025-08-11 05:46:08.705961+00	PENDING		\N		PENDING	2025-08-08 06:11:47.365329+00	\N	 No Incoming calls
122	Not Acquired	+91 97781 60974		MEDIUM		WHATSAPP		2025-08-07 10:28:59.932772+00	2025-10-06 09:11:01.172924+00	5		ENQUIRY	2025-08-11 05:50:30.4342+00	PENDING		\N		PENDING	2025-08-07 10:28:59.93275+00	\N	NAC
165	Jhonson	7593056455		MEDIUM		WHATSAPP		2025-08-08 09:52:28.115004+00	2025-10-06 09:31:56.272739+00	8	Ausbildung	Not Interested	2025-08-22 05:43:11.819932+00	PENDING		\N		PENDING	2025-08-08 09:52:28.114977+00	\N	Already student
154	Not Acquired	6380431192		MEDIUM		WHATSAPP		2025-08-08 06:06:13.80865+00	2025-08-14 10:59:06.677872+00	9	Ausbildung	ENQUIRY	2025-08-11 05:46:21.09788+00	PENDING		\N		PENDING	2025-08-08 06:06:13.808626+00	\N	NAC
159	Not Acquired	9207930114		MEDIUM		WHATSAPP		2025-08-08 06:10:03.71496+00	2025-08-14 10:56:05.141884+00	9	\N	ENQUIRY	2025-08-11 05:46:12.954847+00	PENDING		\N		PENDING	2025-08-08 06:10:03.714935+00	\N	NAC
157	Not Acquired	9100457081		MEDIUM		WHATSAPP		2025-08-08 06:08:17.000569+00	2025-08-14 10:58:22.462917+00	9	Medicine	ENQUIRY	2025-08-11 05:46:15.738225+00	PENDING		\N		PENDING	2025-08-08 06:08:17.000544+00	\N	wrong Number
156	Not Acquired	9496237789		MEDIUM		WHATSAPP		2025-08-08 06:07:23.625235+00	2025-08-14 10:58:29.713028+00	9	\N	ENQUIRY	2025-08-11 05:46:17.736692+00	PENDING		\N		PENDING	2025-08-08 06:07:23.62521+00	\N	NAC
148	Not Acquired	8301974125		MEDIUM		WHATSAPP		2025-08-08 05:59:13.223536+00	2025-08-22 05:18:07.877994+00	8	\N	ENQUIRY	2025-08-22 05:18:07.875926+00	PENDING		\N		PENDING	2025-08-08 05:59:13.223512+00	\N	Already contacted
137	Not Acquired	+91 90742 15945		MEDIUM		WHATSAPP		2025-08-07 10:41:21.341625+00	2025-08-11 05:49:11.592179+00	11	\N	ENQUIRY	2025-08-11 05:49:11.589296+00	PENDING		\N		PENDING	2025-08-07 10:41:21.341598+00	\N	\N
155	Not Acquired	8421700841		MEDIUM		WHATSAPP		2025-08-08 06:06:45.615839+00	2025-08-14 10:58:42.242616+00	9	\N	ENQUIRY	2025-08-11 05:46:19.450429+00	PENDING		\N		PENDING	2025-08-08 06:06:45.615815+00	\N	wrong number
139	Nandu	8281635053		MEDIUM		INSTAGRAM		2025-08-07 11:33:45.656273+00	2025-08-11 05:49:07.862522+00	11	Studies	ENQUIRY	2025-08-11 05:49:07.859523+00	PENDING		\N		PENDING	2025-08-07 11:33:45.656247+00	\N	\N
152	Not Acquired	9074426056		MEDIUM		WHATSAPP		2025-08-08 06:04:58.61346+00	2025-08-22 05:40:14.196227+00	8	Spain	ENQUIRY	2025-08-22 05:40:14.188466+00	PENDING		\N		PENDING	2025-08-08 06:04:58.613436+00	\N	NAC
149	Not Acquired	8119986874		MEDIUM		WHATSAPP		2025-08-08 05:59:57.636165+00	2025-08-22 05:18:16.503801+00	8	\N	ENQUIRY	2025-08-22 05:18:16.500204+00	PENDING		\N		PENDING	2025-08-08 05:59:57.63614+00	\N	NAC
119	Not Acquired	+91 97037 58453		MEDIUM		WHATSAPP		2025-08-07 10:26:45.574504+00	2025-08-18 10:01:15.091907+00	5	\N	ENQUIRY	2025-08-11 05:50:37.173224+00	PENDING		\N		PENDING	2025-08-07 10:26:45.574482+00	\N	NAC
118	Not Acquired	+91 6282246906		MEDIUM		WHATSAPP		2025-08-07 10:26:33.61886+00	2025-08-18 10:02:09.390494+00	5	\N	ENQUIRY	2025-08-11 05:50:38.778282+00	PENDING		\N		PENDING	2025-08-07 10:26:33.618837+00	\N	NAC
116	Not Acquired	+91 87149 37242		MEDIUM		WHATSAPP		2025-08-07 10:24:55.159524+00	2025-08-18 10:12:40.007152+00	5	\N	ENQUIRY	2025-08-11 05:50:42.356295+00	PENDING		\N		PENDING	2025-08-07 10:24:55.159495+00	\N	details shared in whatsapp
163	Not Acquired	9446177850		MEDIUM		WHATSAPP		2025-08-08 06:13:07.515047+00	2025-08-19 08:08:18.723586+00	8	GCC/Estep	NOT_INTERESTED	2025-08-12 11:02:04.189133+00	PENDING		\N		PENDING	2025-08-08 06:13:07.515024+00	\N	Not interested
114	Not Acquired	+91 79029 97443		MEDIUM		WHATSAPP		2025-08-07 09:55:17.091052+00	2025-08-18 10:20:22.331809+00	5	\N	ENQUIRY	2025-08-11 05:50:45.668177+00	PENDING		\N		PENDING	2025-08-07 09:55:17.091028+00	\N	NAC
189	Not Acquired	9745721635	\N	MEDIUM	\N	WHATSAPP	\N	2025-08-27 04:46:21.608715+00	2025-08-27 04:46:21.608719+00	\N	\N	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-08-27 04:46:21.608691+00	\N	\N
147	Not Acquired	9400558766		MEDIUM		WHATSAPP		2025-08-08 05:58:31.07309+00	2025-08-22 05:46:57.847658+00	8	\N	ENQUIRY	2025-08-22 05:18:06.471379+00	PENDING		\N		PENDING	2025-08-08 05:58:31.073066+00	2025-08-12 11:02:58.666965+00	NAC
190	Not Acquired	+971506324571	\N	MEDIUM	\N	WHATSAPP	\N	2025-08-27 04:47:12.572151+00	2025-08-27 04:47:12.572156+00	\N	\N	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-08-27 04:47:12.572127+00	\N	\N
191	Not Acquired	7736548080	\N	MEDIUM	\N	WHATSAPP	\N	2025-08-27 04:48:00.41394+00	2025-08-27 04:48:00.413944+00	\N	\N	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-08-27 04:48:00.413914+00	\N	\N
146	Not Acquired	9400558766		MEDIUM		WHATSAPP		2025-08-08 05:58:31.005326+00	2025-08-11 05:48:45.168167+00	11	\N	ENQUIRY	2025-08-11 05:48:45.164516+00	PENDING		\N		PENDING	2025-08-08 05:58:31.005302+00	\N	\N
145	Not Acquired	8210651551		MEDIUM		WHATSAPP		2025-08-08 05:57:54.787114+00	2025-08-11 05:48:47.008534+00	11	\N	ENQUIRY	2025-08-11 05:48:47.005487+00	PENDING		\N		PENDING	2025-08-08 05:57:54.787088+00	\N	\N
144	Not Acquired	9581312232		MEDIUM		WHATSAPP		2025-08-08 05:57:18.62181+00	2025-08-11 05:48:49.39967+00	11	\N	ENQUIRY	2025-08-11 05:48:49.396695+00	PENDING		\N		PENDING	2025-08-08 05:57:18.621784+00	\N	\N
142	Not Acquired	8590053306		MEDIUM		WHATSAPP		2025-08-08 05:55:16.255918+00	2025-08-11 05:48:57.305277+00	11	\N	ENQUIRY	2025-08-11 05:48:57.302542+00	PENDING		\N		PENDING	2025-08-08 05:55:16.255892+00	\N	\N
141	Not Acquired	9207543152		MEDIUM		WHATSAPP		2025-08-08 05:54:30.020173+00	2025-08-11 05:48:59.6098+00	11	\N	ENQUIRY	2025-08-11 05:48:59.607013+00	PENDING		\N		PENDING	2025-08-08 05:54:30.020148+00	\N	\N
140	Nifal Xavier	9207291641		MEDIUM		INSTAGRAM		2025-08-07 11:34:25.144183+00	2025-08-11 05:49:06.107436+00	11	\N	ENQUIRY	2025-08-11 05:49:06.103814+00	PENDING		\N		PENDING	2025-08-07 11:34:25.144157+00	\N	\N
138	Ajay Krishna	9544191769		MEDIUM		INSTAGRAM		2025-08-07 11:32:37.0037+00	2025-08-11 05:49:10.125514+00	11	Studies	ENQUIRY	2025-08-11 05:49:10.121094+00	PENDING		\N		PENDING	2025-08-07 11:32:37.003672+00	\N	\N
136	Anandhu	+91 70250 87883		MEDIUM		WHATSAPP		2025-08-07 10:40:56.538283+00	2025-08-11 05:49:13.175866+00	11	\N	ENQUIRY	2025-08-11 05:49:13.173021+00	PENDING		\N		PENDING	2025-08-07 10:40:56.538258+00	\N	\N
135	Not Acquired	+91 83980 03126		MEDIUM		WHATSAPP		2025-08-07 10:40:31.114637+00	2025-08-11 05:49:16.29191+00	11	\N	ENQUIRY	2025-08-11 05:49:16.287688+00	PENDING		\N		PENDING	2025-08-07 10:40:31.11461+00	\N	\N
133	Not Acquired	+91 77361 46628		MEDIUM		WHATSAPP		2025-08-07 10:35:06.059947+00	2025-08-11 05:49:19.314103+00	11	\N	ENQUIRY	2025-08-11 05:49:19.311573+00	PENDING		\N		PENDING	2025-08-07 10:35:06.059925+00	\N	\N
132	Not Acquired	+91 94171 94813		MEDIUM		WHATSAPP		2025-08-07 10:34:41.583299+00	2025-08-11 05:49:21.746732+00	11	\N	ENQUIRY	2025-08-11 05:49:21.744387+00	PENDING		\N		PENDING	2025-08-07 10:34:41.583277+00	\N	\N
131	Not Acquired	+91 85805 08427		MEDIUM		WHATSAPP		2025-08-07 10:34:17.139066+00	2025-08-11 05:49:23.169446+00	11	\N	ENQUIRY	2025-08-11 05:49:23.166628+00	PENDING		\N		PENDING	2025-08-07 10:34:17.139043+00	\N	\N
130	Not Acquired	+91 79933 61100		MEDIUM		WHATSAPP		2025-08-07 10:33:49.682686+00	2025-08-11 05:49:24.819635+00	11	Clinical Pharmacy course	ENQUIRY	2025-08-11 05:49:24.816871+00	PENDING		\N		PENDING	2025-08-07 10:33:49.682663+00	\N	\N
129	Not Acquired	+91 80892 60700		MEDIUM		WHATSAPP		2025-08-07 10:32:57.438889+00	2025-08-11 05:49:26.616877+00	11	jobs	ENQUIRY	2025-08-11 05:49:26.614249+00	PENDING		\N		PENDING	2025-08-07 10:32:57.438866+00	\N	\N
128	Not Acquired	+91 73063 45461		MEDIUM		WHATSAPP		2025-08-07 10:32:20.7419+00	2025-08-11 05:49:27.944993+00	11	\N	ENQUIRY	2025-08-11 05:49:27.942352+00	PENDING		\N		PENDING	2025-08-07 10:32:20.741878+00	\N	\N
127	Not Acquired	+91 98763 84978		MEDIUM		WHATSAPP		2025-08-07 10:31:51.803079+00	2025-08-11 05:49:30.24843+00	11	\N	ENQUIRY	2025-08-11 05:49:30.244497+00	PENDING		\N		PENDING	2025-08-07 10:31:51.803057+00	\N	\N
200	Thomas Varghese	8281517470		MEDIUM		INSTAGRAM	\N	2025-09-29 04:31:41.036662+00	2025-10-03 06:21:21.826912+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-29 04:31:41.036635+00	\N	
201	Albin Shaju	8129070840		MEDIUM		INSTAGRAM	\N	2025-09-29 04:35:54.529825+00	2025-10-03 06:21:32.667761+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-29 04:35:54.5298+00	\N	
202	Alen jose	8590207318		MEDIUM		INSTAGRAM	\N	2025-09-29 04:36:16.210204+00	2025-10-03 06:22:05.449608+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-29 04:36:16.210178+00	\N	
125	Not Acquired	+91 80758 85198		MEDIUM		WHATSAPP		2025-08-07 10:30:43.216556+00	2025-08-13 11:27:18.383498+00	5	\N	ENQUIRY	2025-08-11 05:50:25.258389+00	PENDING		\N		PENDING	2025-08-07 10:30:43.216535+00	\N	gcc graphics designer,shared assessment form
236	Akhilesh	7025065986		MEDIUM		INSTAGRAM	\N	2025-10-01 10:37:18.482473+00	2025-10-03 06:27:59.016723+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-01 10:37:18.482444+00	\N	
51	SEBIN	+916238 917 871		MEDIUM		WHATSAPP		2025-08-06 07:03:42.604847+00	2025-08-18 05:25:08.1665+00	11	\N	ENQUIRY	2025-08-18 05:25:08.162656+00	PENDING		\N		PENDING	2025-08-06 07:03:42.604822+00	\N	\N
164	Sooraj	9048157623		MEDIUM		WHATSAPP		2025-08-08 06:14:07.311205+00	2025-08-14 09:27:15.252901+00	9	GCC/ Hospitality and Tourisam	INTERESTED	2025-08-11 05:46:02.130615+00	PENDING		\N		PENDING	2025-08-08 06:14:07.311178+00	2025-08-08 08:57:57.325145+00	Send message
11	Not Aquired	+91 73065 74107		MEDIUM		WHATSAPP		2025-08-06 06:18:05.204455+00	2025-08-18 05:26:57.479472+00	5	\N	ENQUIRY	2025-08-18 05:26:32.379228+00	PENDING		\N		PENDING	2025-08-06 06:18:05.204423+00	\N	\N
143	Haffiz pareed	8137824533		MEDIUM	Ernakulam	WHATSAPP		2025-08-08 05:56:42.964307+00	2025-08-11 05:48:55.74321+00	11	Jobs	ENQUIRY	2025-08-11 05:48:55.74041+00	PENDING		\N		PENDING	2025-08-08 05:56:42.964282+00	\N	\N
134	Not Acquired	+91 83980 03126		MEDIUM		WHATSAPP		2025-08-07 10:40:30.976955+00	2025-08-11 05:49:17.715205+00	11	\N	ENQUIRY	2025-08-11 05:49:17.712326+00	PENDING		\N		PENDING	2025-08-07 10:40:30.976923+00	\N	\N
68	Not Acquired	+91 70251 58066		MEDIUM		WHATSAPP		2025-08-06 07:22:30.78134+00	2025-08-14 09:54:38.882194+00	8	GCC	ENQUIRY	2025-08-12 10:57:37.252358+00	PENDING		\N		PENDING	2025-08-06 07:22:30.781316+00	\N	Details shared
65	Not Acquired	+91 80898 93186		MEDIUM		WHATSAPP		2025-08-06 07:20:08.492187+00	2025-08-14 10:28:59.480873+00	8	GCC	ENQUIRY	2025-08-12 11:02:13.880312+00	PENDING		\N		PENDING	2025-08-06 07:20:08.492154+00	\N	Interested-Logistics
26	AISWARYA	6238 261 725		MEDIUM		WHATSAPP		2025-08-06 06:35:03.316325+00	2025-08-18 09:13:45.414993+00	8	\N	ENQUIRY	2025-08-18 06:16:01.317407+00	PENDING		\N		PENDING	2025-08-06 06:35:03.316299+00	\N	       NAC                   
126	Not Acquired	+91 73062 14825		MEDIUM		WHATSAPP		2025-08-07 10:31:09.789984+00	2025-10-21 05:35:28.684737+00	5	master.MA eng or management course	INTERESTED	2025-08-11 05:50:23.115496+00	PENDING		\N		PENDING	2025-08-07 10:31:09.789962+00	2025-10-21 05:35:06.259491+00	attend call
120	Not Acquired	+91 75608 08619		MEDIUM		WHATSAPP		2025-08-07 10:27:11.753396+00	2025-08-18 09:59:32.029438+00	5	GCC	INTERESTED	2025-08-11 05:50:33.362469+00	PENDING		\N		PENDING	2025-08-07 10:27:11.753374+00	\N	attend call
117	Not Acquired	+91 70342 65093		MEDIUM		WHATSAPP		2025-08-07 10:25:19.357794+00	2025-08-18 10:03:14.817051+00	5	\N	ENQUIRY	2025-08-11 05:50:40.339076+00	PENDING		\N		PENDING	2025-08-07 10:25:19.357772+00	\N	NAC
158	JITHU	8139848498		MEDIUM		WHATSAPP		2025-08-08 06:09:02.314873+00	2025-08-14 10:58:12.004591+00	9	GCC	NOT_INTERESTED	2025-08-11 05:46:14.160525+00	PENDING		\N		PENDING	2025-08-08 06:09:02.314848+00	\N	BBA
192	Not Acquired	7592836131	\N	MEDIUM	\N	AUTOMATION	\N	2025-08-27 04:49:12.930378+00	2025-08-27 04:49:12.930383+00	\N	\N	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-08-27 04:49:12.930355+00	\N	\N
193	Not Acquired	+65 94665752	\N	MEDIUM	\N	WHATSAPP	\N	2025-08-27 08:53:10.690879+00	2025-08-27 08:53:10.690884+00	\N	\N	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-08-27 08:53:10.690854+00	\N	\N
113	Not Acquired	+91 79029 97443		MEDIUM		WHATSAPP		2025-08-07 09:55:16.042323+00	2025-08-18 10:20:34.915612+00	5	\N	ENQUIRY	2025-08-11 05:50:47.448022+00	PENDING		\N		PENDING	2025-08-07 09:55:16.042297+00	\N	same number
20	PARVATHY RAJ	+91 95267 84551		MEDIUM		WHATSAPP		2025-08-06 06:28:11.288068+00	2025-08-18 11:11:08.916332+00	8	\N	ENQUIRY	2025-08-18 06:15:41.950468+00	PENDING		\N		PENDING	2025-08-06 06:28:11.288041+00	\N	Already on processing
43	Not Acquired	6263 347 926		MEDIUM		WHATSAPP		2025-08-06 06:52:28.28279+00	2025-08-18 05:25:22.859682+00	11	\N	ENQUIRY	2025-08-18 05:25:22.856647+00	PENDING		\N		PENDING	2025-08-06 06:52:28.282764+00	\N	\N
35	Not Aquired	+91 87094 82925		MEDIUM		WHATSAPP		2025-08-06 06:42:58.945623+00	2025-08-18 05:25:39.436336+00	11	\N	ENQUIRY	2025-08-18 05:25:39.43269+00	PENDING		\N		PENDING	2025-08-06 06:42:58.945599+00	\N	\N
183	Surya	8301040449	\N	MEDIUM	\N	WHATSAPP	\N	2025-08-15 05:29:25.322609+00	2025-08-15 14:48:40.144806+00	9	Masters	ENQUIRY	2025-08-15 05:29:25.321852+00	PENDING	\N	\N	\N	PENDING	2025-08-15 05:29:25.322579+00	2025-08-15 10:53:47.453989+00	Trial number
98	Rohit Prasad	+91 85953 90508		MEDIUM		WHATSAPP		2025-08-07 04:19:34.133885+00	2025-09-30 11:30:15.235085+00	12	\N	ENQUIRY	2025-08-11 05:56:48.088228+00	PENDING		\N		PENDING	2025-08-07 04:19:34.133859+00	\N	not available
81	Not Acquired	+91 85479 31660		MEDIUM		WHATSAPP		2025-08-06 07:32:41.446299+00	2025-09-30 11:30:49.031492+00	12	\N	ENQUIRY	2025-08-11 05:57:07.748397+00	PENDING		\N		PENDING	2025-08-06 07:32:41.446277+00	\N	exam preparation enqury,share detials
185	George	7356188397	\N	MEDIUM	Thiruvananthapuram	OTHER	\N	2025-08-18 04:43:22.352546+00	2025-08-18 04:43:22.352551+00	11	Ausbildung	ENQUIRY	2025-08-18 04:43:22.351706+00	PENDING	\N	\N	\N	PENDING	2025-08-18 04:43:22.352514+00	\N	Already complete german language training
19	Antony Abin	+91 96332 35997		MEDIUM		WHATSAPP		2025-08-06 06:27:12.718507+00	2025-08-19 06:06:49.178396+00	8	\N	ENQUIRY	2025-08-18 06:15:39.213032+00	PENDING		\N		PENDING	2025-08-06 06:27:12.718482+00	\N	NAC
187	Elvin James	96879751537	\N	MEDIUM	\N	INSTAGRAM	\N	2025-08-20 07:51:01.831104+00	2025-08-20 07:51:01.831109+00	\N	looking for a sort  course in germany	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-08-20 07:51:01.831077+00	\N	\N
61	Not Acquired	+968 7917 8039		MEDIUM		WHATSAPP		2025-08-06 07:18:01.388148+00	2025-08-19 07:57:01.739272+00	8	Visa available in  europe	ENQUIRY	2025-08-12 11:02:05.640079+00	PENDING		\N		PENDING	2025-08-06 07:18:01.388125+00	\N	   
27	Not Aquired	+91 81390 81554		MEDIUM		WHATSAPP		2025-08-06 06:35:51.730344+00	2025-08-22 05:17:49.987984+00	8	\N	ENQUIRY	2025-08-22 05:17:49.985586+00	PENDING		\N		PENDING	2025-08-06 06:35:51.73032+00	\N	\N
196	Not Acquired	8281517470	\N	MEDIUM	\N	WHATSAPP	\N	2025-08-28 13:10:21.481241+00	2025-08-28 13:10:21.481246+00	\N	\N	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-08-28 13:10:21.481214+00	\N	\N
166	Not Acquired	8281680054		MEDIUM		WHATSAPP		2025-08-08 09:53:23.615341+00	2025-08-22 05:23:03.948062+00	9	\N	ENQUIRY	2025-08-09 11:31:29.045431+00	PENDING		\N		PENDING	2025-08-08 09:53:23.615317+00	2025-08-09 11:36:00.995085+00	NI
150	John	9348352234		MEDIUM		WHATSAPP		2025-08-08 06:01:05.084077+00	2025-08-22 05:40:09.644192+00	8	\N	ENQUIRY	2025-08-22 05:40:09.640818+00	PENDING		\N		PENDING	2025-08-08 06:01:05.084051+00	\N	wrong number
151	Not Acquired	7977711699		MEDIUM		WHATSAPP		2025-08-08 06:01:40.398989+00	2025-08-22 05:40:11.426286+00	8	\N	ENQUIRY	2025-08-22 05:40:11.423472+00	PENDING		\N		PENDING	2025-08-08 06:01:40.398964+00	\N	NAC
80	Not Acquired	+91 81369 66076		MEDIUM		WHATSAPP		2025-08-06 07:32:13.349811+00	2025-08-22 05:49:08.520651+00	8	\N	ENQUIRY	2025-08-22 05:18:04.698651+00	PENDING		\N		PENDING	2025-08-06 07:32:13.349786+00	\N	Not interested
153	Shibin	8943636634		MEDIUM		WHATSAPP		2025-08-08 06:05:34.212433+00	2025-08-22 10:23:05.500419+00	9	GCC	ENQUIRY	2025-08-11 05:46:22.902738+00	PENDING		\N		PENDING	2025-08-08 06:05:34.212395+00	\N	Shared setails
110	Not Acquired	+91 89218 85321		MEDIUM		WHATSAPP		2025-08-07 09:53:34.553145+00	2025-09-02 09:29:14.222326+00	5	ausbildung	INTERESTED	2025-08-11 05:50:52.235438+00	PENDING		\N		PENDING	2025-08-07 09:53:34.55312+00	\N	attend the call
105	Sanjay	+91 95114 38554		LOW		WHATSAPP		2025-08-07 04:28:27.666953+00	2025-09-03 06:05:34.938478+00	5	\N	NOT_INTERESTED	2025-08-11 05:50:57.764446+00	PENDING		\N		PENDING	2025-08-07 04:28:27.666928+00	\N	ATTEND CALL
16	Not Aquired	+91 81294 47682		MEDIUM		WHATSAPP		2025-08-06 06:23:24.15026+00	2025-09-03 06:05:45.543052+00	5	\N	ENQUIRY	2025-08-18 05:26:21.606705+00	PENDING		\N		PENDING	2025-08-06 06:23:24.150236+00	\N	\N
197	Not Acquired	9061485438	\N	MEDIUM	\N	WHATSAPP	\N	2025-08-29 06:28:06.043837+00	2025-09-19 05:05:29.473137+00	\N	\N	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-08-29 06:28:06.043812+00	2025-09-19 05:05:23.460024+00	\N
85	Not Acquired	+91 80756 70862		MEDIUM		WHATSAPP		2025-08-06 07:35:57.233701+00	2025-09-30 11:30:40.930787+00	12	\N	ENQUIRY	2025-08-11 05:57:02.295678+00	PENDING		\N		PENDING	2025-08-06 07:35:57.233677+00	\N	not available
225	Aromal RS	9961973972		MEDIUM		INSTAGRAM	\N	2025-09-30 11:14:05.687853+00	2025-10-03 06:24:57.132955+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 11:14:05.68783+00	\N	
229	Paulson	8138988048	\N	HIGH	Palakad	OTHER	\N	2025-09-30 11:20:07.503814+00	2025-09-30 11:36:58.716098+00	12	gcc	ENQUIRY	2025-09-30 11:20:07.503361+00	PENDING	\N	\N	\N	PENDING	2025-09-30 11:20:07.503786+00	\N	bcom,IELTS expired,accountant(6yr exp),no-language
99	Dilip	+91 93593 58885		MEDIUM		WHATSAPP		2025-08-07 04:20:38.370402+00	2025-09-30 11:30:13.127827+00	12	Masters	ENQUIRY	2025-08-11 05:56:46.214125+00	PENDING		\N		PENDING	2025-08-07 04:20:38.370357+00	\N	49 age ,enqury work visa/study abroad
90	Not Acquired	+91 79076 19538		MEDIUM		WHATSAPP		2025-08-06 07:44:35.942729+00	2025-09-30 11:30:24.902752+00	12	Not sure	ENQUIRY	2025-08-11 05:56:54.531436+00	PENDING		\N		PENDING	2025-08-06 07:44:35.942703+00	2025-08-06 13:03:13.131884+00	he calling back
223	Aswathy	6282800443		MEDIUM		INSTAGRAM	\N	2025-09-30 11:11:54.967972+00	2025-10-03 06:25:23.20493+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 11:11:54.967948+00	\N	
220	Reeja elizabath	7907062645		MEDIUM		WEBSITE	\N	2025-09-30 11:08:57.985638+00	2025-10-03 06:26:32.092044+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 11:08:57.985611+00	\N	
206	joby	8078854210		MEDIUM		INSTAGRAM	\N	2025-09-29 04:45:37.515303+00	2025-10-03 06:21:06.610389+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-29 04:45:37.515274+00	\N	
237	Jerrin Fernandez	7025395948		MEDIUM		INSTAGRAM	\N	2025-10-01 10:39:25.089631+00	2025-10-03 06:20:10.569087+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-01 10:39:25.089608+00	\N	Bsc hotel and catering management
251	Elmi	8590512935	\N	MEDIUM	Vaikkom,Kottayam	OTHER	\N	2025-10-03 03:55:44.632531+00	2025-10-03 03:55:44.632535+00	12	PVP	ENQUIRY	2025-10-03 03:55:44.631773+00	PENDING	\N	\N	\N	PENDING	2025-10-03 03:55:44.632502+00	\N	12th biology ,learned upto b2, appearing for a1,a2 on october
252	Joemol	9895006352	\N	MEDIUM	Perumbavur/EKM	OTHER	\N	2025-10-03 04:39:38.212331+00	2025-10-03 04:39:38.212336+00	12	PVP	ENQUIRY	2025-10-03 04:39:38.211482+00	PENDING	\N	\N	\N	PENDING	2025-10-03 04:39:38.212297+00	\N	22 years/Plus 2-Commerce/learned A1, A2-Asking for Slot booking
253	Joemol	9895006352	\N	MEDIUM	Perumbavur/EKM	OTHER	\N	2025-10-03 04:39:38.37436+00	2025-10-03 04:39:38.374364+00	12	PVP	ENQUIRY	2025-10-03 04:39:38.373956+00	PENDING	\N	\N	\N	PENDING	2025-10-03 04:39:38.374331+00	\N	22 years/Plus 2-Commerce/learned A1, A2-Asking for Slot booking
254	Joemol	9895006352	\N	MEDIUM	Perumbavur/EKM	OTHER	\N	2025-10-03 04:39:38.68965+00	2025-10-03 04:39:38.689654+00	12	PVP	ENQUIRY	2025-10-03 04:39:38.689268+00	PENDING	\N	\N	\N	PENDING	2025-10-03 04:39:38.68962+00	\N	22 years/Plus 2-Commerce/learned A1, A2-Asking for Slot booking
255	Princy	9605269919	\N	MEDIUM	Haripad,Alapuzha	OTHER	\N	2025-10-03 04:41:40.035157+00	2025-10-03 04:41:40.035162+00	12	PVP	ENQUIRY	2025-10-03 04:41:40.034743+00	PENDING	\N	\N	\N	PENDING	2025-10-03 04:41:40.03513+00	\N	23 years/Plus 2-Biology Sc-2 y Diploma(Dialysis)-1.5 y experience/B2 (2 modules got)
256	Jain	8129627472	\N	MEDIUM	KTM(now in Saudi)	OTHER	\N	2025-10-03 04:43:39.130731+00	2025-10-03 04:43:39.130735+00	12	GCC	ENQUIRY	2025-10-03 04:43:39.130342+00	PENDING	\N	\N	\N	PENDING	2025-10-03 04:43:39.130703+00	\N	33 years/BE.EEE-10 year Experience/6 month stayed in Berlin/A1,A2 learned-contract ending on 2026 oct-so looking  for next year.
257	Angel Mary Mathew	9526990623	\N	MEDIUM	Banglore	OTHER	\N	2025-10-03 04:46:38.610026+00	2025-10-03 04:46:38.61003+00	12	GCC	ENQUIRY	2025-10-03 04:46:38.60966+00	PENDING	\N	\N	\N	PENDING	2025-10-03 04:46:38.61+00	\N	25 years/B tech -Bio medical Engineering/1.5 year experience -Ultra sound field
263	Rahul	7026946313		MEDIUM		INSTAGRAM	\N	2025-10-03 05:38:18.608327+00	2025-10-03 06:15:20.529395+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 05:38:18.608301+00	\N	Degree
264	Albi	8547520287		MEDIUM		INSTAGRAM	\N	2025-10-03 05:38:44.496642+00	2025-10-03 06:19:25.177953+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 05:38:44.496619+00	\N	Can you sent msg in WhatsApp
266	Akhilesh	7025065986		MEDIUM		INSTAGRAM	\N	2025-10-03 05:39:31.170496+00	2025-10-03 06:19:07.788263+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 05:39:31.170475+00	\N	
273	Rajeshwari	9590455507		MEDIUM		INSTAGRAM	\N	2025-10-03 05:44:31.18102+00	2025-10-03 06:09:58.977084+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 05:44:31.180997+00	\N	Degree \nWhatsApp message
272	Abhijith vikraman	8129963936		MEDIUM		INSTAGRAM	\N	2025-10-03 05:43:57.155498+00	2025-10-03 06:10:21.778322+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 05:43:57.155477+00	\N	Diploama in piping and structural
270	Dhileep	9037495424		MEDIUM		INSTAGRAM	\N	2025-10-03 05:42:32.599443+00	2025-10-03 06:13:22.581842+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 05:42:32.599421+00	\N	Diploma in chemical engineering
269	Vishnu T P	7025797365		MEDIUM		INSTAGRAM	\N	2025-10-03 05:41:05.457587+00	2025-10-03 06:14:19.497917+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 05:41:05.457563+00	\N	Bsc zoology
265	Adam	9895535106		MEDIUM		INSTAGRAM	\N	2025-10-03 05:39:04.9167+00	2025-10-03 06:15:11.354511+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 05:39:04.916676+00	\N	Graduate \nContact only after 4.00 pm\n
240	𝙇𝙖𝙠𝙨𝙝𝙢𝙞 𝙉𝙖𝙣𝙙𝙖𝙣	8078829849		MEDIUM		INSTAGRAM	\N	2025-10-01 11:02:27.943186+00	2025-10-03 06:19:45.393644+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-01 11:02:27.94316+00	\N	
238	Anseb k a	7356102387		MEDIUM		INSTAGRAM	\N	2025-10-01 10:41:29.528032+00	2025-10-03 06:19:58.673883+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-01 10:41:29.528008+00	\N	BCA with 5+ years of experience
230	Moncy Mathew	9633632504		MEDIUM		INSTAGRAM	\N	2025-09-30 11:29:26.144073+00	2025-10-03 06:23:52.10714+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 11:29:26.144049+00	\N	
228	Jeswin	7012206819		MEDIUM		INSTAGRAM	\N	2025-09-30 11:17:57.956058+00	2025-10-03 06:24:14.190321+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 11:17:57.956034+00	\N	
227	akshay	7510103178		MEDIUM		INSTAGRAM	\N	2025-09-30 11:16:19.800917+00	2025-10-03 06:24:23.548341+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 11:16:19.800893+00	\N	
226	Athul Oh 	9633279773		MEDIUM		INSTAGRAM	\N	2025-09-30 11:15:18.179387+00	2025-10-03 06:24:34.561235+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 11:15:18.179362+00	\N	plus two, German 3 modules passed
224	Jamsheer 	9497530145		MEDIUM		INSTAGRAM	\N	2025-09-30 11:13:01.460346+00	2025-10-03 06:25:11.222695+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 11:13:01.460316+00	\N	only WhatsApp
219	Jins	9074519570		MEDIUM		INSTAGRAM	\N	2025-09-30 04:44:50.473371+00	2025-10-03 06:25:45.951637+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 04:44:50.473348+00	\N	
222	Akhil S	7510152045		MEDIUM		INSTAGRAM	\N	2025-09-30 11:11:33.827406+00	2025-10-03 06:26:12.011587+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 11:11:33.827382+00	\N	
214	AKHIL	9544063636		MEDIUM		INSTAGRAM	\N	2025-09-30 04:34:50.235514+00	2025-10-03 06:26:45.495282+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 04:34:50.235488+00	\N	
211	Syed	8304009686		MEDIUM		INSTAGRAM	\N	2025-09-29 04:57:47.717663+00	2025-10-03 06:26:58.004408+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-29 04:57:47.717644+00	\N	
213	Manu	9744891412		MEDIUM		INSTAGRAM	\N	2025-09-30 04:33:43.023453+00	2025-10-03 06:27:09.972953+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 04:33:43.023428+00	\N	
205	Jamsheer	9497530145		MEDIUM		INSTAGRAM	\N	2025-09-29 04:39:54.471297+00	2025-10-03 06:27:40.486509+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-29 04:39:54.471272+00	\N	(contact whatsap only)
218	Bebin	6238468638		MEDIUM		INSTAGRAM	\N	2025-09-30 04:43:20.159255+00	2025-10-03 06:28:26.647293+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 04:43:20.159231+00	\N	
217	shaindora	8086918861		MEDIUM		INSTAGRAM	\N	2025-09-30 04:42:21.556195+00	2025-10-03 06:28:37.634615+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 04:42:21.55617+00	\N	
216	Arjun laiju	9544485732		MEDIUM		INSTAGRAM	\N	2025-09-30 04:37:53.05511+00	2025-10-03 06:28:48.546355+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 04:37:53.055086+00	\N	
210	Gokul satheesh	8075535858		MEDIUM		INSTAGRAM	\N	2025-09-29 04:56:29.870246+00	2025-10-03 06:30:00.761362+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-29 04:56:29.870225+00	\N	
209	Thansif	9539022717		MEDIUM		INSTAGRAM	\N	2025-09-29 04:53:40.932322+00	2025-10-03 06:30:10.513675+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-29 04:53:40.932302+00	\N	
208	Arun Jaitly	9947922590		MEDIUM		INSTAGRAM	\N	2025-09-29 04:46:20.031455+00	2025-10-03 06:30:19.923307+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-29 04:46:20.031435+00	\N	
204	Josmy Varghese	9562141369		MEDIUM		INSTAGRAM	\N	2025-09-29 04:37:16.365379+00	2025-10-03 06:30:35.296749+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-29 04:37:16.365353+00	\N	
215	Ranjith	9074365809		MEDIUM		INSTAGRAM	\N	2025-09-30 04:36:34.593889+00	2025-10-03 06:31:41.513739+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 04:36:34.593865+00	\N	
293	Francis Selvy	8075912691	\N	MEDIUM	Thrissur	WHATSAPP	\N	2025-10-06 04:45:10.505277+00	2025-10-06 11:42:07.404787+00	12	PVP	ENQUIRY	2025-10-06 04:45:10.504874+00	PENDING	\N	\N	\N	PENDING	2025-10-06 04:45:10.505249+00	\N	26 years-Plus 2-commerce(Maths)/A1  certificate, But A2 failed
271	Bipin lal B	7736179418		MEDIUM		INSTAGRAM	\N	2025-10-03 05:43:21.193384+00	2025-10-03 06:10:41.098549+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 05:43:21.193362+00	\N	degree + 1 year diploma in logistics and supply chain management
276	shyam kumar	8281865554		MEDIUM		INSTAGRAM	\N	2025-10-03 06:08:23.959803+00	2025-10-03 06:13:13.618735+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 06:08:23.959777+00	\N	
268	Jeena janardhanan	8304085423		MEDIUM		INSTAGRAM	\N	2025-10-03 05:40:27.522503+00	2025-10-03 06:14:33.414341+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 05:40:27.52248+00	\N	Sir i have completed my masters degree also having a. B. Ed degree. I am looking for a job in germany. I have passed the B2 full module. Can you provide information regarding this?
267	Amjid Roshan	9495252676		MEDIUM		INSTAGRAM	\N	2025-10-03 05:39:56.206232+00	2025-10-03 06:15:40.305178+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 05:39:56.206211+00	\N	Bsc physics
235	Karthik	7034753146		MEDIUM		INSTAGRAM	\N	2025-10-01 10:32:39.786992+00	2025-10-03 06:20:26.487133+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-01 10:32:39.786968+00	\N	
234	shihaan	6282019252		MEDIUM		INSTAGRAM	\N	2025-10-01 03:59:59.017951+00	2025-10-03 06:20:43.210002+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-01 03:59:59.01793+00	\N	
232	Mufeeda	7736548080		MEDIUM		INSTAGRAM	\N	2025-10-01 03:55:08.037532+00	2025-10-03 06:23:19.814883+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-01 03:55:08.037508+00	\N	
221	Albi 	8547520287		MEDIUM		INSTAGRAM	\N	2025-09-30 11:10:31.089381+00	2025-10-03 06:26:21.374409+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-30 11:10:31.089355+00	\N	msg in WhatsApp
212	Alice Varghese	9605641562		MEDIUM		INSTAGRAM	\N	2025-09-29 12:04:48.407709+00	2025-10-03 06:29:32.852614+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-09-29 12:04:48.407683+00	\N	
284	Isabella	+971565852790	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-03 11:25:09.565366+00	2025-10-03 11:25:09.56537+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-03 11:25:09.565341+00	\N	MBA
285	Nousath	8610809946	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-04 06:27:53.851688+00	2025-10-04 06:27:53.851693+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-04 06:27:53.851664+00	\N	
286	Abin das	7356528221	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-06 04:33:00.154142+00	2025-10-06 04:33:00.154147+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-06 04:33:00.15412+00	\N	Degree
287	Bebin	6238468638	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-06 04:34:04.220684+00	2025-10-06 04:34:04.220688+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-06 04:34:04.220662+00	\N	
288	Alosious Babu	9526449983	\N	MEDIUM	idukki	OTHER	\N	2025-10-06 04:34:25.960652+00	2025-10-06 04:34:25.960655+00	12	PVP	ENQUIRY	2025-10-06 04:34:25.960034+00	PENDING	\N	\N	\N	PENDING	2025-10-06 04:34:25.960628+00	\N	22 years/Plus 2 ,Bio science /3 year Diploma-Biomedical Engineering /1 year Experience.
289	Anu Subhash	9539003472	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-06 04:34:38.741809+00	2025-10-06 04:34:38.741813+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-06 04:34:38.741787+00	\N	
290	Suraj S	70256 54202	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-06 04:35:34.634168+00	2025-10-06 04:35:34.634172+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-06 04:35:34.634148+00	\N	Btech
291	Slowmo	8078305239	\N	MEDIUM	\N	OTHER	\N	2025-10-06 04:38:54.509084+00	2025-10-06 04:38:54.509088+00	12	GCC	ENQUIRY	2025-10-06 04:38:54.508741+00	PENDING	\N	\N	\N	PENDING	2025-10-06 04:38:54.50906+00	\N	23 years-Masters (Botony) 2025/A1,A2-learned,B1 started
292	Arun	8136922590	\N	MEDIUM	TVM	OTHER	\N	2025-10-06 04:43:27.342445+00	2025-10-06 04:43:27.34245+00	12	\N	ENQUIRY	2025-10-06 04:43:27.341692+00	PENDING	\N	\N	\N	PENDING	2025-10-06 04:43:27.342413+00	\N	23 years-BBA/worked in Amazon/6 month experience online-Amazon
300	soumya B R	9995487620	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-07 04:35:17.644901+00	2025-10-07 04:35:17.644905+00	\N	\N	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-07 04:35:17.644878+00	\N	Diploma in Radiological technology\r\nI already have A2 certificate. Currently doing B1\r\nWhich job/ course  can I apply?
301	Jithin	9567836432	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-07 04:35:42.671703+00	2025-10-07 04:35:42.671707+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-07 04:35:42.671679+00	\N	
302	Sabarinath T R	6238128740	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-07 04:36:18.20508+00	2025-10-07 04:36:18.205086+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-07 04:36:18.205057+00	\N	Diploma in Mechanical engineering  Currently pursuing btech in Mechanical
303	Adarsh ‪	+91 6361 484 56	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-07 04:36:44.939812+00	2025-10-07 04:36:44.939818+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-07 04:36:44.93979+00	\N	
304	Unnikrishnan MBA	9497631052	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-07 04:37:07.578186+00	2025-10-07 04:37:07.578191+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-07 04:37:07.578163+00	\N	MBA
305	jackson	8848201337	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-07 04:37:32.942295+00	2025-10-07 04:37:32.9423+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-07 04:37:32.942269+00	\N	currently runnung degree
306	Abhijith Divakar	9061138400	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-07 04:38:20.568741+00	2025-10-07 04:38:20.568745+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-07 04:38:20.568717+00	\N	plustwo
307	Ervin	9809839596	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-07 05:10:15.474613+00	2025-10-07 05:10:15.474618+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-07 05:10:15.474586+00	\N	BTech Automobile Engineering
313	Joel	8848575420	not acquired	MEDIUM	Kottayam	OTHER	\N	2025-10-08 04:31:01.906083+00	2025-10-08 04:31:01.906087+00	12	Ausbildung	ENQUIRY	2025-10-08 04:31:01.900756+00	PENDING	\N	\N	\N	PENDING	2025-10-08 04:31:01.906054+00	\N	50 y-Nurse(daughter BA degree final year-German language training
314	Roshna lal	9745224468	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-08 05:14:10.21395+00	2025-10-08 05:14:10.213955+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-08 05:14:10.213926+00	\N	
315	Surjith Valsan	7034563944	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-08 05:14:35.187699+00	2025-10-08 05:14:35.187703+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-08 05:14:35.187674+00	\N	
316	Williams Antony	7012707306	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-08 05:14:58.927235+00	2025-10-08 05:14:58.92724+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-08 05:14:58.927213+00	\N	
317	Dimple Wilson	7902624028	\N	MEDIUM	\N	WEBSITE	\N	2025-10-08 05:15:34.372616+00	2025-10-08 05:15:34.37262+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-08 05:15:34.372594+00	\N	Software Engineer
318	Jessal K Jebbar  Diploma	+96 6560244044	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-08 06:21:29.111734+00	2025-10-08 06:21:29.111739+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-08 06:21:29.11169+00	\N	Diploma
320	Abhilash	9847525530	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-09 11:38:04.996102+00	2025-10-09 11:38:04.996107+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-09 11:38:04.996078+00	\N	
321	ashi	8921146284	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-09 11:38:29.558667+00	2025-10-09 11:38:29.558672+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-09 11:38:29.558644+00	\N	
322	Prasanth Pm	9526414222	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-09 11:44:18.620481+00	2025-10-09 11:44:18.620487+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-09 11:44:18.620453+00	\N	
323	Prasanth Pm	9526414222	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-09 11:44:20.683443+00	2025-10-09 11:44:20.683449+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-09 11:44:20.683415+00	\N	
324	Nitin Joseph	7736486095	\N	MEDIUM	\N	INSTAGRAM	\N	2025-10-09 11:44:31.150168+00	2025-10-10 09:22:55.53245+00	\N	GCC	ENQUIRY	\N	PENDING	\N	\N	\N	PENDING	2025-10-09 11:44:31.150144+00	\N	
121	Harin	+91 6235 726917		MEDIUM		WHATSAPP		2025-08-07 10:28:24.074462+00	2025-10-21 07:43:17.756711+00	5	German Language Teaching	REGISTERED	2025-08-11 05:50:31.7915+00	PENDING		\N		PENDING	2025-08-07 10:28:24.07444+00	2025-10-21 06:19:37.706634+00	call back.now attend class
339	Risheb.s	7994631745	rishebs@example.com	MEDIUM	Kerala	OTHER	\N	2025-10-22 04:57:31.900557+00	2025-10-22 04:57:31.900584+00	12	BBA	INTERESTED	2025-10-22 04:57:31.896277+00	PENDING	\N	\N	\N	PENDING	2025-10-22 04:57:31.900522+00	\N	Requested callback
\.


--
-- Data for Name: leads_processingupdate; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.leads_processingupdate (id, status, notes, "timestamp", changed_by_id, lead_id) FROM stdin;
\.


--
-- Data for Name: leads_remarkhistory; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.leads_remarkhistory (id, previous_remarks, new_remarks, changed_at, changed_by_id, lead_id) FROM stdin;
1	nac	NAC	2025-08-19 06:19:09.819587+00	5	126
2	NAC	nac	2025-08-19 06:22:06.934775+00	5	126
3	nac	Nac	2025-08-19 06:43:01.593769+00	5	126
4	Nac	NAC	2025-08-19 06:43:51.588858+00	5	126
5	NAC	This is a dummy record for test purposes	2025-08-19 06:44:46.829063+00	5	126
6	This is a dummy record for test purposes	NAC	2025-08-19 06:45:13.406315+00	5	126
7	NAC	nac	2025-08-19 07:03:35.051947+00	5	126
8	NAC	nac	2025-08-19 07:03:35.171802+00	5	126
9	nac	NAC	2025-08-19 07:03:56.849542+00	5	126
10	nac	NAC	2025-08-19 07:03:56.887868+00	5	126
11	NAC	nac	2025-08-19 07:04:43.098918+00	5	126
12	NAC	nac	2025-08-19 07:04:43.227274+00	5	126
13	nac	NAC	2025-08-19 07:05:34.374005+00	5	126
14	NAC	Nac	2025-08-19 07:10:26.739554+00	5	126
15	NAC	Nac	2025-08-19 07:10:26.766176+00	5	126
16	Nac	NAC	2025-08-19 07:11:19.206589+00	5	126
17	Nac	NAC	2025-08-19 07:11:19.436606+00	5	126
24	\N	   	2025-08-19 07:57:01.701338+00	8	61
25	Interested in banking and finance sector,.BCOM& B2 full module completed	Interested 	2025-08-19 08:10:29.911762+00	8	18
28	NAC	NI	2025-08-22 05:23:03.933069+00	9	166
29	\N	NAC	2025-08-22 05:46:57.827898+00	8	147
30	\N	Not interested	2025-08-22 05:49:08.511658+00	8	80
31	\N	NAC	2025-08-22 05:52:23.187127+00	8	63
32	\N	Details share	2025-08-22 05:55:22.154558+00	8	62
33	\N	NAC	2025-08-22 06:00:52.64171+00	8	29
34	NAC	NAC  	2025-08-22 09:13:51.025613+00	8	29
35	\N	NAC	2025-08-27 09:45:29.777726+00	8	25
36	\N	interested	2025-09-02 09:28:57.345348+00	5	110
37	interested	attend the call	2025-09-02 09:29:04.552718+00	5	110
38	NAC	\N	2025-09-03 05:26:41.468722+00	5	126
39	\N	attend call	2025-09-03 05:28:30.331283+00	5	126
40	\N	NAC	2025-09-03 06:00:45.309972+00	5	107
41	\N	NAC	2025-09-03 06:01:56.066046+00	5	106
42	\N	ATTEND CALL	2025-09-03 06:05:21.344469+00	5	105
47	\N	plus two, German 3 modules passed	2025-09-30 11:36:02.952518+00	2	226
48	\N	only WhatsApp	2025-09-30 11:38:18.366022+00	2	224
49	\N	msg in WhatsApp	2025-09-30 11:38:48.70449+00	2	221
50	\N	Bsc hotel and catering management	2025-10-01 10:40:08.351898+00	2	237
51	\N	BCA with 5+ years of experience	2025-10-01 10:41:39.393839+00	2	238
52		Sir i have completed my masters degree also having a. B. Ed degree. I am looking for a job in germany. I have passed the B2 full module. Can you provide information regarding this?	2025-10-03 05:44:54.863781+00	2	268
53		Bsc physics	2025-10-03 05:45:14.650832+00	2	267
54		Graduate \nContact only after 4.00 pm\n	2025-10-03 05:45:40.242496+00	2	265
55		Can you sent msg in WhatsApp	2025-10-03 05:46:08.066714+00	2	264
56		Degree	2025-10-03 05:46:34.099749+00	2	263
57	Degree \r\nWhatsApp message	Degree \nWhatsApp message	2025-10-03 06:09:58.961098+00	2	273
58	\N		2025-10-03 06:19:45.38695+00	2	240
59	\N		2025-10-03 06:20:26.47982+00	2	235
60	\N		2025-10-03 06:20:43.201592+00	2	234
61	\N		2025-10-03 06:21:06.603875+00	2	206
62	\N		2025-10-03 06:21:21.808336+00	2	200
63	\N		2025-10-03 06:21:32.662916+00	2	201
64	\N		2025-10-03 06:22:05.44077+00	2	202
65	\N		2025-10-03 06:23:08.83233+00	2	233
66	\N		2025-10-03 06:23:19.807063+00	2	232
67	\N		2025-10-03 06:23:32.668577+00	2	231
68	\N		2025-10-03 06:23:52.10173+00	2	230
69	\N		2025-10-03 06:24:14.185026+00	2	228
70	\N		2025-10-03 06:24:23.542812+00	2	227
71	\N		2025-10-03 06:24:57.126133+00	2	225
72	\N		2025-10-03 06:25:23.197359+00	2	223
73	\N		2025-10-03 06:25:45.945784+00	2	219
74	\N		2025-10-03 06:26:12.00277+00	2	222
75	\N		2025-10-03 06:26:32.085622+00	2	220
76	\N		2025-10-03 06:26:45.489917+00	2	214
77	\N		2025-10-03 06:26:57.997606+00	2	211
78	\N		2025-10-03 06:27:09.965275+00	2	213
79	\N	(contact whatsap only)	2025-10-03 06:27:40.47922+00	2	205
80	\N		2025-10-03 06:27:59.009203+00	2	236
81	\N		2025-10-03 06:28:26.639343+00	2	218
82	\N		2025-10-03 06:28:37.626628+00	2	217
83	\N		2025-10-03 06:28:48.538271+00	2	216
84	\N		2025-10-03 06:29:32.216043+00	2	212
85	\N		2025-10-03 06:30:00.755225+00	2	210
86	\N		2025-10-03 06:30:10.501428+00	2	209
87	\N		2025-10-03 06:30:19.916021+00	2	208
88	\N		2025-10-03 06:30:35.291129+00	2	204
89	\N		2025-10-03 06:31:41.50522+00	2	215
\.


--
-- Data for Name: tasks_task; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tasks_task (id, title, description, status, priority, deadline, created_at, updated_at, completed_at, assigned_by_id, assigned_to_id) FROM stdin;
9	posting	dummy 2	COMPLETED	MEDIUM	2025-10-10 10:00:00+00	2025-10-10 04:29:12.700437+00	2025-10-10 06:06:57.832824+00	2025-10-10 06:06:57.832824+00	13	2
11	dummy4	dummy task 4	COMPLETED	MEDIUM	2025-10-10 10:31:00+00	2025-10-10 05:00:24.150152+00	2025-10-10 06:07:49.418261+00	2025-10-10 06:07:49.418261+00	13	2
14	dummy 9	dummy task 9	COMPLETED	MEDIUM	2025-10-10 11:49:00+00	2025-10-10 06:18:24.946746+00	2025-10-10 06:19:30.334429+00	2025-10-10 06:19:30.334318+00	13	5
8	report submission	submit the kiosk leads report	COMPLETED	MEDIUM	2025-10-10 07:13:00+00	2025-10-10 01:42:03.423938+00	2025-10-10 06:26:13.367933+00	2025-10-10 06:26:13.367933+00	13	7
6	posting	post video for promotion	OVERDUE	MEDIUM	2025-10-10 07:00:00+00	2025-10-10 01:28:18.407397+00	2025-10-10 08:29:12.24161+00	\N	13	2
7	video shoot	promotion video shoot	OVERDUE	HIGH	2025-10-10 07:10:00+00	2025-10-10 01:38:15.820927+00	2025-10-10 08:29:12.258135+00	\N	13	2
10	dummy3	dummy task 3	OVERDUE	HIGH	2025-10-10 10:13:00+00	2025-10-10 04:42:49.862908+00	2025-10-10 10:14:59.876903+00	\N	13	6
12	dummy5	dummy task 5	OVERDUE	HIGH	2025-10-10 11:00:00+00	2025-10-10 05:29:30.246701+00	2025-10-10 11:04:31.435408+00	\N	13	2
13	dummy6	dummy task 6	OVERDUE	MEDIUM	2025-10-10 11:10:00+00	2025-10-10 05:39:41.133496+00	2025-10-10 11:10:38.875549+00	\N	13	6
15	dummy 10	dummy task 10	OVERDUE	MEDIUM	2025-10-10 14:21:00+00	2025-10-10 08:50:16.670233+00	2025-10-10 16:37:56.200658+00	\N	13	11
16	dummy12	dummy task 12	OVERDUE	MEDIUM	2025-10-11 05:15:00+00	2025-10-11 05:14:05.942244+00	2025-10-11 05:16:19.18604+00	\N	13	2
17	dummy13	dummy task 13	OVERDUE	MEDIUM	2025-10-11 05:18:00+00	2025-10-11 05:17:13.879361+00	2025-10-11 05:19:11.394393+00	\N	13	5
18	dummy 14	dummy task 14	OVERDUE	MEDIUM	2025-10-11 05:46:00+00	2025-10-11 05:45:12.877031+00	2025-10-11 05:47:08.651018+00	\N	13	2
19	dummy 14	dummy task 14	OVERDUE	MEDIUM	2025-10-11 06:02:00+00	2025-10-11 06:01:53.814416+00	2025-10-11 06:02:01.353544+00	\N	13	5
20	dummy20	dummy task 20	OVERDUE	MEDIUM	2025-10-11 06:06:00+00	2025-10-11 06:04:45.219477+00	2025-10-11 06:08:38.233726+00	\N	13	5
21	dummy 10	dummy description	OVERDUE	MEDIUM	2025-10-21 07:59:00+00	2025-10-21 07:27:43.792419+00	2025-10-21 11:22:08.345825+00	\N	13	5
\.


--
-- Data for Name: tasks_taskupdate; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tasks_taskupdate (id, previous_status, new_status, notes, created_at, task_id, updated_by_id) FROM stdin;
3	PENDING	PENDING	Task created by govind venugopal	2025-10-10 01:28:18.426907+00	6	13
4	PENDING	PENDING	Task created by govind venugopal	2025-10-10 01:38:16.11742+00	7	13
5	PENDING	PENDING	Task created by govind venugopal	2025-10-10 01:42:03.429533+00	8	13
6	PENDING	PENDING	Task created by govind venugopal	2025-10-10 04:29:12.713568+00	9	13
7	PENDING	PENDING	Task created by govind venugopal	2025-10-10 04:42:49.90055+00	10	13
8	PENDING	PENDING	Task created by govind venugopal	2025-10-10 05:00:24.405982+00	11	13
9	PENDING	PENDING	Task created by govind venugopal	2025-10-10 05:29:30.267668+00	12	13
10	PENDING	PENDING	Task created by govind venugopal	2025-10-10 05:39:41.473043+00	13	13
11	PENDING	COMPLETED		2025-10-10 06:06:57.569552+00	9	2
12	OVERDUE	COMPLETED		2025-10-10 06:07:49.174408+00	11	2
13	PENDING	PENDING	Task created by govind venugopal	2025-10-10 06:18:24.966053+00	14	13
14	PENDING	COMPLETED		2025-10-10 06:19:30.330625+00	14	5
15	PENDING	COMPLETED		2025-10-10 06:26:13.097728+00	8	7
16	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-10 08:29:12.219396+00	6	13
17	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-10 08:29:12.254388+00	7	13
18	PENDING	PENDING	Task created by govind venugopal	2025-10-10 08:50:16.693112+00	15	13
19	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-10 10:14:59.838071+00	10	13
20	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-10 11:04:31.42051+00	12	13
21	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-10 11:10:38.871478+00	13	13
22	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-10 16:37:56.178154+00	15	13
23	PENDING	PENDING	Task created by govind venugopal	2025-10-11 05:14:06.20568+00	16	13
24	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-11 05:16:18.946995+00	16	13
25	PENDING	PENDING	Task created by govind venugopal	2025-10-11 05:17:14.124113+00	17	13
26	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-11 05:19:11.151729+00	17	13
27	PENDING	PENDING	Task created by govind venugopal	2025-10-11 05:45:13.149907+00	18	13
28	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-11 05:47:08.408675+00	18	13
29	PENDING	PENDING	Task created by govind venugopal	2025-10-11 06:01:54.051698+00	19	13
30	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-11 06:02:01.077189+00	19	13
31	PENDING	PENDING	Task created by govind venugopal	2025-10-11 06:04:45.474042+00	20	13
32	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-11 06:08:37.986492+00	20	13
33	PENDING	PENDING	Task created by govind venugopal	2025-10-21 07:27:43.805058+00	21	13
34	PENDING	OVERDUE	Automatically marked as overdue due to deadline	2025-10-21 11:22:08.325399+00	21	13
\.


--
-- Data for Name: trainers_trainer; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trainers_trainer (id, drive_link, status, user_id) FROM stdin;
1		ACTIVE	10
2		ACTIVE	14
\.


--
-- Data for Name: trainers_student; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.trainers_student (id, name, batch, status, admission_date, notes, trainer_id) FROM stdin;
\.


--
-- Name: accounts_dailyreport_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.accounts_dailyreport_id_seq', 40, true);


--
-- Name: accounts_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.accounts_user_groups_id_seq', 1, false);


--
-- Name: accounts_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.accounts_user_id_seq', 14, true);


--
-- Name: accounts_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.accounts_user_user_permissions_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 64, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 72, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 16, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 42, true);


--
-- Name: hob_hobsetting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hob_hobsetting_id_seq', 1, false);


--
-- Name: leads_lead_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.leads_lead_id_seq', 339, true);


--
-- Name: leads_processingupdate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.leads_processingupdate_id_seq', 10, true);


--
-- Name: leads_remarkhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.leads_remarkhistory_id_seq', 91, true);


--
-- Name: tasks_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tasks_task_id_seq', 21, true);


--
-- Name: tasks_taskupdate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tasks_taskupdate_id_seq', 34, true);


--
-- Name: trainers_student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trainers_student_id_seq', 1, false);


--
-- Name: trainers_trainer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.trainers_trainer_id_seq', 2, true);


--
-- PostgreSQL database dump complete
--

\unrestrict zZr9Kf9NCDlHETjWrzxO6i4kd2lr1dx5m6GtAaXQw1451TW4Woykb3Zt2W7mAjk

