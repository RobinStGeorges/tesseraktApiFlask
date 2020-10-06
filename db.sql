-- borrowed from https://stackoverflow.com/q/7745609/808921

CREATE TABLE IF NOT EXISTS `docs` (
  `id` int(6) unsigned NOT NULL,
  `rev` int(3) unsigned NOT NULL,
  `content` varchar(200) NOT NULL,
  PRIMARY KEY (`id`,`rev`)
) DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `cours` (
`id_cours` int(3) NOT NULL, 
`id_exercice` int(3) NOT NULL, 
`titre` varchar(255) NOT NULL DEFAULT "titre default",
`description` varchar(500) NOT NULL DEFAULT "description default",
`contenue` varchar(2000) NOT NULL DEFAULT "contenue default",
`mediaPath` varchar(255)
)DEFAULT CHARSET=utf8;



CREATE TABLE IF NOT EXISTS `exercice`(
`id_exercice` int(3) NOT NULL, 
`titre` varchar(255) NOT NULL DEFAULT "titre default",
`description` varchar(500) NOT NULL DEFAULT "description default",
`contenue` varchar(2000) NOT NULL DEFAULT "contenue default",
`mediaPath` varchar(255),
`id_reponse` int(3),
`imgPath` varchar(255),
`imgReponsePath` varchar(255),
`cube_needed` varchar(255),
`matrix_size_x` int(3),
`matrix_size_y` int(3),
`disponible` int(3),
`matrix_size_x_board` int(3),
`matrix_size_y_board` int(3),
`coord_finish` varchar(255),
`x_start` int(3),
`y_start` int(3)
);
