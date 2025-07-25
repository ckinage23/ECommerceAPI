INSERT INTO public.users ("name",email,phone,oauth_provider,oauth_sub,"role",hashed_password,is_active) VALUES
	 ('Admin','admin@example.com','9999888823',NULL,NULL,'ADMIN'::public."userrole",'$2b$12$H7EWKo8MSK/E6amYaifK0eWfswelR5SDEbB5mbXuMWXay15sCDKR6',true),
	 ('Chinmayee Kinage','c.doe@example.com','1234567890',NULL,NULL,'CUSTOMER'::public."userrole",'$2b$12$nd6B3wyIz/0oEYdhrQkB8.hCNSmo9YlHlwFGthCWyyP33RExg84oC',true),
	 ('Duplicate User','cc.doe@example.com','8888710134',NULL,NULL,'CUSTOMER'::public."userrole",'$2b$12$axp2Mh6GN.amzbf/wDxKUugsBWenoxEQ0pH3BZOe.A2bh3NCbjn.2',true);
