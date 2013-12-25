create table players (
	id varchar(50) primary key,
	name varchar(100) not null,
	position varchar(10) not null,
	height int,
	weight int,
	url varchar(100) not null
);
create index players_position_idx on players(position);

create table season_totals (
	id int auto_increment primary key,
	player_id varchar(50) not null,
	season int not null,
	age int not null,
	team varchar(3) not null,
	league varchar(3) not null,
	position varchar(2) not null,
	games int not null,
	games_started int not null,
	minutes_played int not null,
	field_goals int not null,
	field_goal_attempts int not null,
	field_goal_pct float not null,
	three_point_field_goals int not null,
	three_point_field_goal_attempts int not null,
	three_point_field_goal_pct float not null,
	two_point_field_goals int not null,
	two_point_field_goal_attempts int not null,
	two_point_field_goal_pct float not null,
	free_throws int not null,
	free_throw_attempts int not null,
	free_throw_pct float not null,
	offensive_rebounds int not null,
	defensive_rebounds int not null,
	total_rebounds int not null,
	assists int not null,
	steals int not null,
	blocks int not null,
	turnovers int not null,
	personal_fouls int not null,
	points int not null,
	foreign key (player_id) references players(id)
);

create table season_advanced (
	id int auto_increment primary key,
	player_id varchar(50) not null,
	season int not null,
	age int not null,
	team varchar(3) not null,
	league varchar(3) not null,
	position varchar(2) not null,
	games int not null,
	minutes_played int not null,
	player_efficiency_rating float not null,
	true_shooting_pct float not null,
	effective_field_goal_pct float not null,
	free_throw_attempt_rate float not null,
	three_point_field_goal_attempt_rate float not null,
	offensive_rebound_pct float not null,
	defensive_rebound_pct float not null,
	total_rebound_pct float not null,
	assist_pct float not null,
	steal_pct float not null,
	block_pct float not null,
	turnover_pct float not null,
	usage_pct float not null,
	offensive_rating int not null,
	defensive_rating int not null,
	offensive_win_shares float not null,
	defensive_win_shares float not null,
	win_shares float not null,
	win_shares_per_48_minutes float not null,
	foreign key (player_id) references players(id)
);

create table game_totals_basic (
	id integer auto_increment primary key,
	player_id varchar(50) not null,
	season int not null,
	game_number int not null,
	date timestamp not null,
	age int not null,
	team varchar(3) not null,
	home boolean not null,
	opponent varchar(3) not null,
	result varchar(10) not null,
	games_started int not null,
	minutes_played float not null,
	field_goals int not null,
	field_goal_attempts int not null,
	field_goal_pct float not null,
	three_point_field_goals int not null,
	three_point_field_goal_attempts int not null,
	three_point_field_goal_pct float not null,
	free_throws int not null,
	free_throw_attempts int not null,
	free_throw_pct float not null,
	offensive_rebounds int not null,
	defensive_rebounds int not null,
	total_rebounds int not null,
	assists int not null,
	steals int not null,
	blocks int not null,
	turnovers int not null,
	personal_fouls int not null,
	points int not null,
	game_score float not null,
	plus_minus int not null,
	foreign key (player_id) references players(id)
);
create index game_totals_basic_season_idx on game_totals_basic(season);
create index game_totals_basic_date_idx on game_totals_basic(date);
create index game_totals_basic_team_idx on game_totals_basic(team);

create table game_totals_advanced (
	id int auto_increment primary key,
	player_id varchar(50) not null,
	season int not null,
	game_number int not null,
	date timestamp not null,
	age int not null,
	team varchar(3) not null,
	home boolean not null,
	opponent varchar(3) not null,
	result varchar(10) not null,
	games_started int not null,
	minutes_played float not null,
	true_shooting_pct float not null,
	effective_field_goal_pct float not null,
	offensive_rebound_pct float not null,
	defensive_rebound_pct float not null,
	total_rebound_pct float not null,
	assist_pct float not null,
	steal_pct float not null,
	block_pct float not null,
	turnover_pct float not null,
	usage_pct float not null,
	offensive_rating int not null,
	defensive_rating int not null,
	game_score float not null,
	foreign key (player_id) references players(id)
);
create index game_totals_advanced_season_idx on game_totals_advanced(season);
create index game_totals_advanced_date_idx on game_totals_advanced(date);

create table splits (
	id int auto_increment primary key,
	player_id varchar(50) not null,
	season int not null,
	type varchar(50) not null,
	subtype varchar(50) not null,
	games int not null,
	games_started int not null,
	minutes_played int not null,
	field_goals int not null,
	field_goal_attempts int not null,
	three_point_field_goals int not null,
	three_point_field_goal_attempts int not null,
	free_throws int not null,
	free_throw_attempts int not null,
	offensive_rebounds int not null,
	defensive_rebounds int not null,
	total_rebounds int not null,
	assists int not null,
	steals int not null,
	blocks int not null,
	turnovers int not null,
	personal_fouls int not null,
	points int not null,
	field_goal_pct float not null,
	three_point_field_goal_pct float not null,
	free_throw_pct float not null,
	true_shooting_pct float not null,
	offensive_rating int not null,
	defensive_rating int not null,
	plus_minus float,
	minutes_played_per_game float not null,
	points_per_game float not null,
	total_rebounds_per_game float not null,
	assists_per_game float not null,
	foreign key (player_id) references players(id)
);

/*
 * Team tables
 */
create table team_game_totals(
	id int auto_increment primary key,
	team varchar(3) not null,
	season int not null,
	game int not null,
	date timestamp not null,
	home boolean not null,
	opponent varchar(3) not null,
	result varchar(1) not null,
	minutes_played int not null,
	field_goals float not null,
	field_goal_attempts float not null,
	three_point_field_goals float not null,
	three_point_field_goal_attempts float not null,
	free_throws float not null,
	free_throw_attempts float not null,
	offensive_rebounds float not null,
	total_rebounds float not null,
	assists float not null,
	steals float not null,
	blocks float not null,
	turnovers float not null,
	personal_fouls float not null,
	points float not null,
	opp_field_goals float not null,
	opp_field_goal_attempts float not null,
	opp_three_point_field_goals float not null,
	opp_three_point_field_goal_attempts float not null,
	opp_free_throws float not null,
	opp_free_throw_attempts float not null,
	opp_offensive_rebounds float not null,
	opp_total_rebounds float not null,
	opp_assists float not null,
	opp_steals float not null,
	opp_blocks float not null,
	opp_turnovers float not null,
	opp_personal_fouls float not null,
	opp_points float not null
);
create index team_game_totals_team_idx on team_game_totals(team);
create index team_game_totals_season_idx on team_game_totals(season);
create index team_game_totals_date_idx on team_game_totals(date);

create table team_splits(
	id int auto_increment primary key,
	team varchar(3) not null,
	season int not null,
	type varchar(50) not null,
	subtype varchar(50) not null,
	games int not null,
	wins int not null,
	losses int not null,
	field_goals float not null,
	field_goal_attempts float not null,
	three_point_field_goals float not null,
	three_point_field_goal_attempts float not null,
	free_throws float not null,
	free_throw_attempts float not null,
	offensive_rebounds float not null,
	total_rebounds float not null,
	assists float not null,
	steals float not null,
	blocks float not null,
	turnovers float not null,
	personal_fouls float not null,
	points float not null,
	opp_field_goals float not null,
	opp_field_goal_attempts float not null,
	opp_three_point_field_goals float not null,
	opp_three_point_field_goal_attempts float not null,
	opp_free_throws float not null,
	opp_free_throw_attempts float not null,
	opp_offensive_rebounds float not null,
	opp_total_rebounds float not null,
	opp_assists float not null,
	opp_steals float not null,
	opp_blocks float not null,
	opp_turnovers float not null,
	opp_personal_fouls float not null,
	opp_points float not null
);

create table salaries (
	id int auto_increment primary key,
	player_id varchar(100) not null,
	site varchar(50) not null,
	salary int not null,
	date timestamp not null default CURRENT_TIMESTAMP,
	foreign key (player_id) references players(id)
);

create table fantasy_points (
	id int auto_increment primary key,
	game_totals_basic_id int not null,
	player_id varchar(100) not null,
	site varchar(50) not null,
	season int not null,
	game_number int not null,
	points float not null,
	foreign key (player_id) references players(id),
	foreign key (game_totals_basic_id) references game_totals_basic(id)
);
create index fantasy_points_site_idx on fantasy_points(site);
create unique index fantasy_points_player_id_site_season_game_number_idx on fantasy_points(player_id, site, season, game_number);

create table schedules (
	id int auto_increment primary key,
	season int not null,
	date date not null,
	visitor varchar(3) not null,
	home varchar(3) not null
);
create index schedules_date_idx on schedules(date);
create index schedules_visitor_idx on schedules(visitor);
create index schedules_home_idx on schedules(home);

create table dfs_site_positions (
	id int auto_increment primary key,
	player_id varchar(100) not null,
	site varchar(50) not null,
	position varchar(10) not null,
	foreign key (player_id) references players(id)
);
create index dfs_site_positions_player_id_idx on dfs_site_positions(player_id);
create index dfs_site_positions_player_site_idx on dfs_site_positions(site);