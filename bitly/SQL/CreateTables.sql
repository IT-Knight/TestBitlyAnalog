
CREATE TABLE IF NOT EXISTS dbo.Users (
    ID UUID PRIMARY Key UNIQUE NOT NULL DEFAULT uuid_generate_v4(),
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_on TIMESTAMPZ NOT NULL DEFAULT NOW()
)

CREATE TABLE IF NOT EXISTS dbo.Links (
	user_id UUID,
	link VARCHAR(300) NOT NULL,
	short_link VARCHAR(300) NOT NULL,
	CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES dbo.Users(ID) ON DELETE CASCADE
)


INSERT INTO dbo.Users(username, email, password) VALUES (
    'admin', 'admin@admin.com', '123'
)