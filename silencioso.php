<?php

// app/Models/Event.php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Event extends Model
{
    protected $fillable = [
        'title',
        'description',
        'date',
        'location',
    ];
}

// app/Models/User.php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    protected $fillable = [
        'name',
        'email',
    ];
}

// Exemplo de uso:
$event = new Event();
$event->title = 'Community Meeting';
$event->description = 'Monthly community meeting';
$event->date = '2023-03-15';
$event->location = 'City Hall';
$event->save();

$user = new User();
$user->name = 'John Doe';
$user->email = 'johndoe@example.com';
$user->save();

echo "Event and User data saved successfully.\n";

?>
