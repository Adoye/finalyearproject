<?php
$name = $_POST['name'];
$email = $_POST['email'];
$subject = $_POST['subject'];
$message = $_POST['message'];
$formcontent = " From: $name \n subject: $subject \n  Message: $message";
$recipient = "info@cmslab.net";
$mailheader = 'From:' . $email;
if(mail($recipient, $subject, $formcontent, $mailheader)){
	header("location: thank-you.html");
}else{
	echo 'Mail Not Sent';
}