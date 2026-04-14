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

        <form id="connexion" action="connexion.php">
            <fieldset>
                <legend>Connexion</legend>

                <label for="login">Identifiant :</label>
                <input type="text" name="login" required>
            
                </br>

                <label for="password">Mot de passe :</label>
                <input type="password" name="password" required>

                </br>

                <label for="submit" ></label>
                <button type="button" class="inscription" name="submit">Se connecter</button>

                <p>Vous n'avez pas encore de compte ? <a href="inscription.php">Inscrivez-vous</a></p>

            </fieldset>
        </form>


        <br><br>
        <div>
            <span >Nous contacter :</span>
            <p>Email : contact@cpp.com<br/>Téléphone : 01 23 45 67 89</p>
            <br/>
        </div>
        
    </body>
</php>
