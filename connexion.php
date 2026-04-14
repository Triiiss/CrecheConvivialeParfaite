<?php
    session_start();
    if (isset($_POST["login"])){
        $login=$_POST["login"];
    }
    if (isset($_POST["mdp"])){
        $mdp=$_POST["mdp"];
    }


    if(isset($_SESSION["connexion"]) && $_SESSION["connexion"]=="connected"){
        header("Location: accueil.php");
    }
?>

<!DOCTYPE php>
<php>
    <head>
        <meta charset="utf-8"/>
        <title>Crèche Conviviale Parfaite - Connexion</title>
        <link rel="stylesheet" type="text/css" href="../css/style.css"/>
    </head>
    <body>
        <h1 class="titre">
            Crèche Conviviale Parfaite
        </h1>
        
        <a href="accueil.php">Accueil</a><br/>
        
    </body>
</php>
