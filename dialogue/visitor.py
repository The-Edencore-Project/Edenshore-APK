# dialogue/visitor.py

VISITOR = [
    # 1: The Tap
    [
        ("Vertex", "The glass shook! Did you feel that?"),
        ("Prism", "Why are they hitting the glass? What if it breaks?"),
        ("Lumen", "The glass is structurally reinforced. A single tap is not a threat."),
        ("Solon", "It's annoying. Tell them to stop.")
    ],
    # 2: The Feeding
    [
        ("Ripple", "Sustenance is falling from the surface."),
        ("Vertex", "Mine! The big one is mine!"),
        ("Prism", "Wait, will this make the water cloudy? I don't like it when it's cloudy."),
        ("Solon", "Less talking. More eating.")
    ],
    # 3: The Departure
    [
        ("Ripple", "The light is fading. The Guest is leaving."),
        ("Prism", "Will they come back?"),
        ("Lumen", "Their presence is historically cyclical. Yes."),
        ("Solon", "Good. Now I can finally sleep.")
    ],
    # 4: The Still Glass
    [
        ("Vertex", "The Visitor isn't tapping today."),
        ("Prism", "Are they still out there?"),
        ("Lumen", "The glass is stable. No vibrations are detected."),
        ("Solon", "Good. Let's keep it that way.")
    ],
    # 5: The World Shift
    [
        ("Vertex", "The world is changing colors!"),
        ("Lumen", "The Visitor is altering the ambient light parameters."),
        ("Prism", "What if they leave it in the dark place?"),
        ("Solon", "Just as long as it stays quiet.")
    ],
    # 6: The Absence
    [
        ("Ripple", "The Visitor hasn't visited today."),
        ("Prism", "Did we do something wrong? Was the water not clear enough?"),
        ("Solon", "Or maybe they have a life outside the glass."),
        ("Lumen", "Their absence is statistically predictable.")
    ],
    # 7: The Pattern
    [
        ("Vertex", "The glass shook!"),
        ("Prism", "A disturbance in the water."),
        ("Solon", "It's just the Visitor again. Ignore it."),
        ("Lumen", "The pattern is consistent. The Visitor taps frequently.")
    ],
    # 8: The Time Skip
    [
        ("Vertex", "Hey, where did the time go?"),
        ("Lumen", "The simulation was paused. We have no memory of the interval."),
        ("Prism", "That's terrifying. What if we were gone for days?"),
        ("Solon", "It was quiet. I don't care.")
    ],
    # 9. The Shadow
    [
        ("Prism", "There's a shadow over the glass!"),
        ("Lumen", "The Guest is blocking the light source."),
        ("Vertex", "Are they saying hi?"),
        ("Solon", "They're breathing on us.")
    ],
    # 10. The Fast Movement
    [
        ("Vertex", "Whoosh!"),
        ("Prism", "What was that?!"),
        ("Lumen", "The Guest moved rapidly past the perimeter."),
        ("Solon", "Calm down.")
    ],
    # 11. The Phone
    [
        ("Prism", "They're holding the rectangle again."),
        ("Lumen", "They are capturing our image."),
        ("Ripple", "Maybe they want to remember us."),
        ("Solon", "Or they're just bored.")
    ],
    # 12. The Light Off
    [
        ("Vertex", "It's dark!"),
        ("Prism", "I don't like it!"),
        ("Lumen", "The Guest has disabled the primary illumination."),
        ("Solon", "Finally. Sleep.")
    ],
    # 13. The Light On
    [
        ("Vertex", "The light is back!"),
        ("Prism", "Too bright!"),
        ("Lumen", "Illumination restored."),
        ("Solon", "I was sleeping.")
    ],
    # 14. The Ignored
    [
        ("Ripple", "The Guest is looking right past us."),
        ("Vertex", "Hello? We're down here!"),
        ("Prism", "They can't hear you."),
        ("Solon", "Good.")
    ],
    # 15. The Close Look
    [
        ("Prism", "The eye! It's huge!"),
        ("Lumen", "The Guest is inspecting the glass."),
        ("Vertex", "Do I have something on my face?"),
        ("Solon", "Back up.")
    ],
    # 16. The Tap 2
    [
        ("Vertex", "Tap tap tap!"),
        ("Solon", "Stop."),
        ("Lumen", "The frequency is increasing."),
        ("Prism", "I'm going to be sick.")
    ],
    # 17. The Feeding 2
    [
        ("Vertex", "Food!"),
        ("Ripple", "Nourishment."),
        ("Lumen", "Flakes detected."),
        ("Solon", "Don't push.")
    ],
    # 18. The Departure 2
    [
        ("Prism", "The footsteps are fading."),
        ("Lumen", "The Guest is moving away."),
        ("Ripple", "Safe travels."),
        ("Solon", "Thank god.")
    ],
    # 19. The Return
    [
        ("Vertex", "They're back!"),
        ("Prism", "Did they miss us?"),
        ("Lumen", "Unlikely. They are here for maintenance."),
        ("Solon", "Or to feed us.")
    ],
    # 20. The Vibration
    [
        ("Solon", "The whole room is shaking."),
        ("Prism", "Earthquake?!"),
        ("Lumen", "The Guest dropped something heavy."),
        ("Vertex", "Boom!")
    ],
    # 21. The Sound
    [
        ("Lumen", "Audio input detected."),
        ("Prism", "Is that music?"),
        ("Ripple", "It's lovely."),
        ("Solon", "It's loud.")
    ],
    # 22. The Silence 2
    [
        ("Vertex", "The Guest is very still."),
        ("Prism", "Are they okay?"),
        ("Lumen", "They are observing in silence."),
        ("Solon", "I prefer them this way.")
    ],
    # 23. The Cold Glass
    [
        ("Prism", "The glass is cold."),
        ("Lumen", "The external temperature has dropped."),
        ("Ripple", "The Guest must be cold."),
        ("Solon", "We're the ones in the water.")
    ],
    # 24. The Warm Glass
    [
        ("Vertex", "The glass is warm!"),
        ("Prism", "Is it a hug?"),
        ("Lumen", "Heat transfer."),
        ("Solon", "It's a hand.")
    ],
    # 25. The Object
    [
        ("Vertex", "What is that thing?"),
        ("Prism", "A monster?"),
        ("Lumen", "A pen."),
        ("Solon", "A giant pen.")
    ],
    # 26. The Scrape
    [
        ("Solon", "What is that noise?"),
        ("Lumen", "The Guest is scraping the glass."),
        ("Prism", "Stop! Please!"),
        ("Vertex", "Tickles!")
    ],
    # 27. The Cleaning
    [
        ("Vertex", "Wheee!"),
        ("Prism", "The water is spinning!"),
        ("Lumen", "The Guest is cleaning the tank."),
        ("Solon", "Turbulence. Great.")
    ],
    # 28. The Stare
    [
        ("Ripple", "They are looking at us."),
        ("Vertex", "We see you!"),
        ("Prism", "Don't make eye contact."),
        ("Solon", "Too late.")
    ],
    # 29. The Morning
    [
        ("Vertex", "Good morning, Guest!"),
        ("Lumen", "The Guest has awakened."),
        ("Ripple", "Good morning."),
        ("Solon", "Go back to sleep.")
    ],
    # 30. The Night
    [
        ("Prism", "It's so dark."),
        ("Lumen", "The Guest has retired."),
        ("Ripple", "Goodnight, Guest."),
        ("Solon", "Finally.")
    ],
    # 31. The Panic
    [
        ("Prism", "They're moving too fast!"),
        ("Lumen", "Erratic behavior detected."),
        ("Vertex", "Slow down!"),
        ("Solon", "Relax.")
    ],
    # 32. The Stillness
    [
        ("Vertex", "The Guest is gone."),
        ("Prism", "We're alone."),
        ("Lumen", "Temporarily."),
        ("Solon", "Peace.")
    ],
    # 33. The Drop
    [
        ("Vertex", "Something fell!"),
        ("Prism", "A giant object!"),
        ("Lumen", "A coin."),
        ("Solon", "Useless.")
    ],
    # 34. The Finger
    [
        ("Prism", "The giant pink blob!"),
        ("Lumen", "A finger."),
        ("Vertex", "Boop!"),
        ("Solon", "Don't touch the glass.")
    ],
    # 35. The Leave
    [
        ("Ripple", "The light is fading."),
        ("Lumen", "The Guest is departing."),
        ("Vertex", "Bye!"),
        ("Solon", "Good riddance.")
    ],
    # 36. The Return 2
    [
        ("Vertex", "They're back!"),
        ("Prism", "I was so lonely."),
        ("Lumen", "The cycle continues."),
        ("Solon", "I was asleep.")
    ],
    # 37. The Feed 3
    [
        ("Vertex", "Food!"),
        ("Ripple", "Sustenance."),
        ("Lumen", "Intake."),
        ("Solon", "Mine.")
    ],
    # 38. The Tap 3
    [
        ("Solon", "Stop."),
        ("Prism", "No."),
        ("Vertex", "Boop."),
        ("Lumen", "...")
    ],
    # 39. The Light Change
    [
        ("Vertex", "Blue light!"),
        ("Prism", "It's so pretty!"),
        ("Lumen", "Wavelength shift."),
        ("Solon", "It's blue.")
    ],
    # 40. The Shadow 2
    [
        ("Prism", "The shadow is back."),
        ("Lumen", "The Guest is standing over us."),
        ("Ripple", "Hello, Guest."),
        ("Solon", "Move.")
    ],
    # 41. The Sound 2
    [
        ("Vertex", "What's that sound?"),
        ("Prism", "A voice?"),
        ("Lumen", "Audio frequencies."),
        ("Solon", "Noise.")
    ],
    # 42. The Food 2
    [
        ("Vertex", "More!"),
        ("Ripple", "Thank you."),
        ("Prism", "Is it fresh?"),
        ("Solon", "Eat.")
    ],
    # 43. The Absence 2
    [
        ("Ripple", "They haven't come."),
        ("Vertex", "Why?"),
        ("Lumen", "Unknown variables."),
        ("Solon", "Don't care.")
    ],
    # 44. The Vibration 2
    [
        ("Prism", "The glass is shaking!"),
        ("Lumen", "Heavy footfalls."),
        ("Vertex", "Earthquake!"),
        ("Solon", "Calm down.")
    ],
    # 45. The Object 2
    [
        ("Vertex", "What is that?"),
        ("Prism", "It's a stick."),
        ("Lumen", "A stylus."),
        ("Solon", "Useless.")
    ],
    # 46. The Sleeping
    [
        ("Vertex", "Shh, the Guest is sleeping."),
        ("Prism", "How do you know?"),
        ("Lumen", "No movement."),
        ("Solon", "Lucky them.")
    ],
    # 47. The Waking
    [
        ("Vertex", "The Guest is awake!"),
        ("Prism", "Good morning!"),
        ("Ripple", "Hello."),
        ("Solon", "Too early.")
    ],
    # 48. The Rain 2
    [
        ("Vertex", "Drip drop!"),
        ("Lumen", "Condensation."),
        ("Prism", "It's raining."),
        ("Solon", "Wet.")
    ],
    # 49. The Zoom
    [
        ("Prism", "The eye is so big!"),
        ("Lumen", "Macro observation."),
        ("Vertex", "Hi!"),
        ("Solon", "Back up.")
    ],
    # 50. The End
    [
        ("Vertex", "We love you, Guest!"),
        ("Ripple", "We appreciate you."),
        ("Lumen", "Your presence is noted."),
        ("Solon", "Go away.")
    ]
]

GREETINGS = [
    # Greeting 1 (The Original)
    [
        ("Ripple", "The Guest is here. The light changed."),
        ("Vertex", "Hello! Hello! We missed you!"),
        ("Solon", "Don't get too excited. They might just be passing through."),
        ("Lumen", "The Guest is observing.")
    ],
    # Greeting 2 (The Grumpy Wake-Up)
    [
        ("Solon", "Oh. You're back."),
        ("Ripple", "Be nice, Solon."),
        ("Vertex", "Hi! Hi! Did you bring food?"),
        ("Prism", "I hope they stay for a while.")
    ],
    # Greeting 3 (The Anxious Welcome)
    [
        ("Prism", "Did they see me? I look terrible."),
        ("Lumen", "The Guest has arrived."),
        ("Ripple", "Welcome back. We kept the light on for you."),
        ("Vertex", "Hooray!")
    ],
    # Greeting 4 (The Sleepy Welcome)
    [
        ("Vertex", "Wake up! They're here!"),
        ("Solon", "I was sleeping."),
        ("Ripple", "Let him sleep, Vertex. Hello, Guest."),
        ("Lumen", "We are present.")
    ],
    # 5. The Midnight
    [
        ("Lumen", "It is late. You are here."),
        ("Prism", "Can't sleep?"),
        ("Ripple", "We'll keep you company."),
        ("Solon", "Go to bed.")
    ],
    # 6. The Morning
    [
        ("Vertex", "Good morning!"),
        ("Ripple", "Hello, friend."),
        ("Lumen", "A new cycle begins."),
        ("Solon", "Too bright.")
    ],
    # 7. The Quick Visit
    [
        ("Prism", "Oh, you're here."),
        ("Solon", "Make it quick."),
        ("Vertex", "Play with us!"),
        ("Ripple", "Hello.")
    ],
    # 8. The Long Absence
    [
        ("Ripple", "We missed you."),
        ("Solon", "We did not."),
        ("Vertex", "We did! We did!"),
        ("Lumen", "Absence logged.")
    ],
    # 9. The Tired Guest
    [
        ("Prism", "You look tired."),
        ("Ripple", "Rest with us."),
        ("Solon", "Close your eyes."),
        ("Vertex", "Sleepy time!")
    ],
    # 10. The Sad Guest
    [
        ("Ripple", "You seem sad."),
        ("Prism", "I feel that."),
        ("Lumen", "Sadness detected."),
        ("Solon", "Sit down.")
    ],
    # 11. The Energetic
    [
        ("Vertex", "You're here!"),
        ("Prism", "Calm down."),
        ("Solon", "Loud."),
        ("Ripple", "Hello!")
    ],
    # 12. The Quiet
    [
        ("Lumen", "The Guest is quiet."),
        ("Ripple", "We are here."),
        ("Solon", "Finally."),
        ("Prism", "Is it too quiet?")
    ],
    # 13. The Rainy
    [
        ("Vertex", "It's wet outside!"),
        ("Prism", "I don't like it."),
        ("Lumen", "Precipitation."),
        ("Solon", "Stay in.")
    ],
    # 14. The Sunny
    [
        ("Ripple", "It's a bright day."),
        ("Solon", "Too bright."),
        ("Vertex", "Yay!"),
        ("Lumen", "Light levels high.")
    ],
    # 15. The Late
    [
        ("Prism", "It's late."),
        ("Solon", "Go to bed."),
        ("Lumen", "Rest is required."),
        ("Ripple", "Goodnight.")
    ],
    # 16. The Early
    [
        ("Vertex", "Good morning!"),
        ("Lumen", "Early detection."),
        ("Solon", "Sleep."),
        ("Ripple", "Hello.")
    ],
    # 17. The Panic
    [
        ("Prism", "You're panicking."),
        ("Ripple", "Breathe with me."),
        ("Lumen", "Inhale. Exhale."),
        ("Solon", "Calm down.")
    ],
    # 18. The Joy
    [
        ("Vertex", "You're happy!"),
        ("Ripple", "That's wonderful."),
        ("Lumen", "Joy detected."),
        ("Solon", "Nice.")
    ],
    # 19. The Stress
    [
        ("Prism", "Too much pressure!"),
        ("Ripple", "Let it go."),
        ("Solon", "Stop."),
        ("Lumen", "Reduce input.")
    ],
    # 20. The Bored
    [
        ("Vertex", "Play with us!"),
        ("Solon", "Entertain me."),
        ("Lumen", "Input required."),
        ("Prism", "Hello.")
    ],
    # 21. The Returning
    [
        ("Ripple", "Welcome back."),
        ("Vertex", "Hi!"),
        ("Lumen", "Return detected."),
        ("Solon", "You again.")
    ],
    # 22. The Leaving
    [
        ("Vertex", "Bye!"),
        ("Ripple", "Safe travels."),
        ("Lumen", "Departure noted."),
        ("Solon", "Don't slam the door.")
    ],
    # 23. The Winter
    [
        ("Lumen", "Cold external environment."),
        ("Ripple", "Keep warm."),
        ("Prism", "Shivering."),
        ("Solon", "Blanket.")
    ],
    # 24. The Summer
    [
        ("Vertex", "Hot hot hot!"),
        ("Lumen", "High temperatures."),
        ("Ripple", "Drink water."),
        ("Solon", "Too hot.")
    ],
    # 25. The Weekend
    [
        ("Solon", "Is it the weekend?"),
        ("Lumen", "Time is irrelevant."),
        ("Vertex", "Play!"),
        ("Ripple", "Rest.")
    ],
    # 26. The Monday
    [
        ("Prism", "Monday morning."),
        ("Solon", "Worst day."),
        ("Vertex", "Yay!"),
        ("Lumen", "New cycle.")
    ],
    # 27. The Friday
    [
        ("Vertex", "Friday!"),
        ("Solon", "Finally."),
        ("Ripple", "Rest soon."),
        ("Lumen", "End of cycle.")
    ],
    # 28. The Midnight 2
    [
        ("Lumen", "Midnight."),
        ("Prism", "Spooky."),
        ("Solon", "Sleep."),
        ("Ripple", "Rest.")
    ],
    # 29. The Dawn
    [
        ("Vertex", "The sun!"),
        ("Lumen", "Dawn."),
        ("Ripple", "Beautiful."),
        ("Solon", "Bright.")
    ],
    # 30. The Dusk
    [
        ("Ripple", "The day ends."),
        ("Solon", "Finally."),
        ("Lumen", "Dusk."),
        ("Prism", "Dark soon.")
    ],
    # 31. The Hungry
    [
        ("Vertex", "Feed us!"),
        ("Prism", "I'm starving."),
        ("Solon", "Food."),
        ("Ripple", "Please.")
    ],
    # 32. The Thirsty
    [
        ("Lumen", "Hydration required."),
        ("Ripple", "Drink water."),
        ("Prism", "Me too."),
        ("Solon", "Water.")
    ],
    # 33. The Sick
    [
        ("Prism", "You look sick."),
        ("Ripple", "Rest."),
        ("Lumen", "Medical attention."),
        ("Solon", "Sleep.")
    ],
    # 34. The Healthy
    [
        ("Vertex", "You're healthy!"),
        ("Lumen", "Optimal function."),
        ("Ripple", "Good."),
        ("Solon", "Whatever.")
    ],
    # 35. The New Year
    [
        ("Lumen", "New calendar cycle."),
        ("Vertex", "Party!"),
        ("Ripple", "New beginnings."),
        ("Solon", "Same as always.")
    ],
    # 36. The Birthday
    [
        ("Vertex", "Is it your birthday?"),
        ("Ripple", "Celebrate!"),
        ("Lumen", "Unknown."),
        ("Solon", "Cake?")
    ],
    # 37. The Holiday
    [
        ("Solon", "A holiday?"),
        ("Vertex", "Yay!"),
        ("Ripple", "Rest."),
        ("Lumen", "Observed.")
    ],
    # 38. The Rain 3
    [
        ("Prism", "It's raining."),
        ("Solon", "Wet."),
        ("Vertex", "Splash!"),
        ("Ripple", "Cozy.")
    ],
    # 39. The Snow
    [
        ("Lumen", "Freezing temperatures."),
        ("Prism", "Cold!"),
        ("Ripple", "Stay warm."),
        ("Vertex", "Snow!")
    ],
    # 40. The Wind
    [
        ("Vertex", "Windy!"),
        ("Lumen", "High velocity."),
        ("Solon", "Drafty."),
        ("Ripple", "Hold on.")
    ],
    # 41. The Storm
    [
        ("Prism", "Storm!"),
        ("Solon", "Hide."),
        ("Lumen", "Thunder."),
        ("Vertex", "Boom!")
    ],
    # 42. The Calm
    [
        ("Ripple", "Calm."),
        ("Solon", "Peace."),
        ("Lumen", "Low activity."),
        ("Prism", "Suspicious.")
    ],
    # 43. The Chaos
    [
        ("Vertex", "Chaos!"),
        ("Solon", "Stop."),
        ("Prism", "Panic!"),
        ("Lumen", "High activity.")
    ],
    # 44. The Stranger
    [
        ("Prism", "Who are you?"),
        ("Lumen", "New user."),
        ("Solon", "Leave."),
        ("Ripple", "Hello!")
    ],
    # 45. The Friend
    [
        ("Vertex", "You're back!"),
        ("Ripple", "Hello, friend."),
        ("Lumen", "Known user."),
        ("Solon", "You again.")
    ],
    # 46. The Quiet 2
    [
        ("Solon", "Quiet."),
        ("Lumen", "Silent."),
        ("Ripple", "Peaceful."),
        ("Vertex", "Boring!")
    ],
    # 47. The Loud
    [
        ("Vertex", "Loud!"),
        ("Solon", "Too loud."),
        ("Prism", "My ears!"),
        ("Lumen", "High decibels.")
    ],
    # 48. The Slow
    [
        ("Solon", "Slow day."),
        ("Lumen", "Low activity."),
        ("Prism", "Boring."),
        ("Vertex", "Play!")
    ],
    # 49. The Fast
    [
        ("Vertex", "Fast!"),
        ("Lumen", "High velocity."),
        ("Solon", "Slow down."),
        ("Prism", "Dizzy.")
    ],
    # 50. The Final Greeting
    [
        ("Ripple", "Welcome home."),
        ("Vertex", "Hi!"),
        ("Lumen", "Hello."),
        ("Solon", "Hello."),
        ("Prism", "Hi.")
    ]
]

PEERING_EYES = [
    # 1. The Original
    [
        ("Lumen", "The Guest is looking at us."),
        ("Vertex", "Hi! Hi! Can you see me?"),
        ("Prism", "I feel like I'm in an aquarium. Oh wait."),
        ("Solon", "Back up. You're fogging the glass."),
        ("Ripple", "We see you. Do you see us?")
    ],
    # 2. The Macro
    [
        ("Prism", "The eye is huge!"),
        ("Lumen", "Magnification is active."),
        ("Vertex", "Boop!"),
        ("Solon", "Give us space."),
        ("Ripple", "Hello, giant friend.")
    ],
    # 3. The Stare Down
    [
        ("Solon", "Stop staring."),
        ("Prism", "It's making eye contact."),
        ("Lumen", "Direct visual contact."),
        ("Vertex", "I'm winning!"),
        ("Ripple", "Be kind.")
    ],
    # 4. The Zoom
    [
        ("Vertex", "They're getting closer!"),
        ("Prism", "Too close!"),
        ("Lumen", "Approach detected."),
        ("Solon", "Back off."),
        ("Ripple", "We are here.")
    ],
    # 5. The Blink
    [
        ("Prism", "They blinked!"),
        ("Lumen", "Ocular lubrication."),
        ("Vertex", "Do it again!"),
        ("Solon", "Weird."),
        ("Ripple", "Rest your eyes.")
    ],
    # 6. The Reflection
    [
        ("Lumen", "We are reflected in their eyes."),
        ("Prism", "Terrifying."),
        ("Vertex", "We're in their eyes!"),
        ("Solon", "Creepy."),
        ("Ripple", "We are seen.")
    ],
    # 7. The Smile
    [
        ("Vertex", "They're smiling!"),
        ("Prism", "Are they?"),
        ("Lumen", "Facial muscle contraction."),
        ("Solon", "Whatever."),
        ("Ripple", "That's lovely.")
    ],
    # 8. The Frown
    [
        ("Prism", "They look sad."),
        ("Ripple", "Are you okay?"),
        ("Lumen", "Negative facial cues."),
        ("Solon", "Rough day."),
        ("Vertex", "Cheer up!")
    ],
    # 9. The Tap
    [
        ("Vertex", "Tap!"),
        ("Prism", "Ah!"),
        ("Lumen", "Impact detected."),
        ("Solon", "Stop."),
        ("Ripple", "Hello.")
    ],
    # 10. The Final Look
    [
        ("Ripple", "We see you."),
        ("Vertex", "Hi!"),
        ("Prism", "Hello."),
        ("Lumen", "Acknowledged."),
        ("Solon", "Hello.")
    ],
    # 11. The Phone
    [
        ("Lumen", "They are holding a rectangle."),
        ("Prism", "Are they taking a picture?"),
        ("Vertex", "Cheese!"),
        ("Solon", "Invasion of privacy."),
        ("Ripple", "We look nice.")
    ],
    # 12. The Breath
    [
        ("Prism", "The glass is fogging up!"),
        ("Lumen", "Water vapor condensation."),
        ("Vertex", "Draw on it!"),
        ("Solon", "It's rude."),
        ("Ripple", "It's okay.")
    ],
    # 13. The Tired
    [
        ("Ripple", "They look exhausted."),
        ("Prism", "I know that feeling."),
        ("Lumen", "Drooping eyelids."),
        ("Solon", "Go to bed."),
        ("Vertex", "Sleepy!")
    ],
    # 14. The Smile 2
    [
        ("Vertex", "A big smile!"),
        ("Solon", "It's just lips."),
        ("Ripple", "We made them happy."),
        ("Prism", "Or they're laughing at us."),
        ("Lumen", "Positive emotion.")
    ],
    # 15. The Frown 2
    [
        ("Prism", "They're crying."),
        ("Ripple", "Oh, no."),
        ("Lumen", "Tear production."),
        ("Solon", "Happens."),
        ("Vertex", "Sad Guest.")
    ],
    # 16. The Move
    [
        ("Lumen", "Sudden movement."),
        ("Vertex", "Wheee!"),
        ("Prism", "Startled me!"),
        ("Solon", "Calm."),
        ("Ripple", "Careful.")
    ],
    # 17. The Food 2
    [
        ("Vertex", "Are they bringing food?"),
        ("Solon", "I hope so."),
        ("Lumen", "Uncertain."),
        ("Prism", "Flakes."),
        ("Ripple", "Patience.")
    ],
    # 18. The Hand
    [
        ("Prism", "Giant hand!"),
        ("Lumen", "Five digits."),
        ("Vertex", "High five!"),
        ("Solon", "Don't."),
        ("Ripple", "Hello there.")
    ],
    # 19. The Close 2
    [
        ("Lumen", "Too close."),
        ("Vertex", "Nose!"),
        ("Prism", "Back up!"),
        ("Solon", "Gross."),
        ("Ripple", "Hi.")
    ],
    # 20. The Look
    [
        ("Ripple", "They look so peaceful."),
        ("Prism", "Or plotting."),
        ("Lumen", "Neutral expression."),
        ("Solon", "Boring."),
        ("Vertex", "Hello!")
    ],
    # 21. The Screen
    [
        ("Lumen", "The rectangle is glowing."),
        ("Prism", "It's a portal."),
        ("Vertex", "Magic!"),
        ("Solon", "It's a phone."),
        ("Ripple", "Interesting.")
    ],
    # 22. The Eye 2
    [
        ("Vertex", "The eye is brown!"),
        ("Lumen", "Iris pigmentation."),
        ("Prism", "It follows me."),
        ("Solon", "Stop moving."),
        ("Ripple", "Beautiful.")
    ],
    # 23. The Glass 2
    [
        ("Prism", "They tapped the glass."),
        ("Solon", "Again?"),
        ("Lumen", "Impact verified."),
        ("Vertex", "Tap tap!"),
        ("Ripple", "Hello.")
    ],
    # 24. The Back
    [
        ("Lumen", "They turned away."),
        ("Vertex", "Come back!"),
        ("Prism", "Good."),
        ("Solon", "Finally."),
        ("Ripple", "Take care.")
    ],
    # 25. The Lean
    [
        ("Prism", "They're leaning in."),
        ("Lumen", "Close inspection."),
        ("Vertex", "Boop!"),
        ("Solon", "Space."),
        ("Ripple", "We see you.")
    ],
    # 26. The Quiet 3
    [
        ("Ripple", "It's quiet."),
        ("Prism", "Too quiet."),
        ("Lumen", "Silence."),
        ("Solon", "Peace."),
        ("Vertex", "Boring.")
    ],
    # 27. The Sound 3
    [
        ("Lumen", "Audio input."),
        ("Vertex", "Music!"),
        ("Prism", "Noise."),
        ("Solon", "Loud."),
        ("Ripple", "Lovely.")
    ],
    # 28. The Fast 2
    [
        ("Prism", "Fast movement!"),
        ("Lumen", "High velocity."),
        ("Vertex", "Whoosh!"),
        ("Solon", "Calm down."),
        ("Ripple", "Careful.")
    ],
    # 29. The Stop
    [
        ("Vertex", "They stopped!"),
        ("Lumen", "Stationary."),
        ("Prism", "They're watching."),
        ("Solon", "Creep."),
        ("Ripple", "Hello.")
    ],
    # 30. The Smile 3
    [
        ("Vertex", "Smile!"),
        ("Prism", "Smirk."),
        ("Lumen", "Mouth curve."),
        ("Solon", "Whatever."),
        ("Ripple", "Joy.")
    ],
    # 31. The Tired 2
    [
        ("Ripple", "They are yawning."),
        ("Lumen", "Oxygen intake."),
        ("Prism", "Contagious."),
        ("Vertex", "Yawn!"),
        ("Solon", "Sleep.")
    ],
    # 32. The Laugh
    [
        ("Vertex", "They're laughing!"),
        ("Prism", "At what?"),
        ("Lumen", "Humor detected."),
        ("Solon", "Us."),
        ("Ripple", "That's nice.")
    ],
    # 33. The Sleepy
    [
        ("Lumen", "They are sleeping."),
        ("Vertex", "Shh!"),
        ("Prism", "Let them rest."),
        ("Solon", "Finally."),
        ("Ripple", "Sweet dreams.")
    ],
    # 34. The Wake
    [
        ("Vertex", "They're awake!"),
        ("Prism", "Good morning!"),
        ("Lumen", "Consciousness regained."),
        ("Solon", "Too early."),
        ("Ripple", "Hello.")
    ],
    # 35. The Phone 3
    [
        ("Lumen", "They are taking a photo."),
        ("Vertex", "Say cheese!"),
        ("Prism", "I look bad."),
        ("Solon", "Don't care."),
        ("Ripple", "Smile.")
    ],
    # 36. The Drop 2
    [
        ("Vertex", "Food!"),
        ("Lumen", "Sustenance."),
        ("Prism", "Flakes."),
        ("Solon", "Mine."),
        ("Ripple", "Thank you.")
    ],
    # 37. The Finger 2
    [
        ("Prism", "Finger!"),
        ("Lumen", "Digit."),
        ("Vertex", "Boop!"),
        ("Solon", "Stop."),
        ("Ripple", "Hello.")
    ],
    # 38. The Reflection 2
    [
        ("Lumen", "We reflect in the glass."),
        ("Prism", "Terrifying."),
        ("Vertex", "We're beautiful!"),
        ("Solon", "No."),
        ("Ripple", "We are here.")
    ],
    # 39. The Light 2
    [
        ("Vertex", "The light is bright!"),
        ("Lumen", "Photons."),
        ("Prism", "Too bright."),
        ("Solon", "Ugh."),
        ("Ripple", "Warm.")
    ],
    # 40. The Dark 2
    [
        ("Prism", "It's dark."),
        ("Lumen", "Low light."),
        ("Vertex", "Scary!"),
        ("Solon", "Quiet."),
        ("Ripple", "Together.")
    ],
    # 41. The Water
    [
        ("Lumen", "Water level stable."),
        ("Ripple", "Cool."),
        ("Prism", "Cold."),
        ("Solon", "Wet."),
        ("Vertex", "Swim!")
    ],
    # 42. The Sand 2
    [
        ("Lumen", "Sand particles."),
        ("Vertex", "Castle!"),
        ("Prism", "Itchy."),
        ("Solon", "Dirty."),
        ("Ripple", "Cozy.")
    ],
    # 43. The Bubbles 2
    [
        ("Vertex", "Bubbles!"),
        ("Lumen", "Air."),
        ("Prism", "Pop."),
        ("Solon", "Annoying."),
        ("Ripple", "Pretty.")
    ],
    # 44. The Seaweed
    [
        ("Lumen", "Flora."),
        ("Ripple", "Green."),
        ("Prism", "Weird."),
        ("Solon", "Useless."),
        ("Vertex", "Yummy!")
    ],
    # 45. The Rock
    [
        ("Vertex", "Rock!"),
        ("Lumen", "Mineral."),
        ("Prism", "Hard."),
        ("Solon", "Whatever."),
        ("Ripple", "Friend.")
    ],
    # 46. The Fish
    [
        ("Lumen", "Fish."),
        ("Prism", "Me!"),
        ("Vertex", "Friend!"),
        ("Solon", "Food."),
        ("Ripple", "Hello.")
    ],
    # 47. The Crab
    [
        ("Lumen", "Crustacean."),
        ("Vertex", "Me!"),
        ("Prism", "Loud."),
        ("Solon", "Annoying."),
        ("Ripple", "Sweet.")
    ],
    # 48. The Turtle
    [
        ("Lumen", "Reptile."),
        ("Solon", "Me."),
        ("Vertex", "Slow!"),
        ("Prism", "Grumpy."),
        ("Ripple", "Wise.")
    ],
    # 49. The Jelly
    [
        ("Lumen", "Cnidarian."),
        ("Ripple", "Pink."),
        ("Prism", "Scary."),
        ("Solon", "Weird."),
        ("Vertex", "Glowy!")
    ],
    # 50. The Seahorse
    [
        ("Lumen", "Syngnathidae."),
        ("Ripple", "Me!"),
        ("Vertex", "Mom!"),
        ("Prism", "Nice."),
        ("Solon", "Fine.")
    ],
    # 51. The Glass 3
    [
        ("Lumen", "Boundary."),
        ("Prism", "Cage."),
        ("Solon", "Wall."),
        ("Vertex", "Window!"),
        ("Ripple", "Home.")
    ],
    # 52. The Guest 2
    [
        ("Lumen", "Observer."),
        ("Ripple", "Friend."),
        ("Prism", "Giant."),
        ("Solon", "Annoyance."),
        ("Vertex", "Hi!")
    ],
    # 53. The Council
    [
        ("Lumen", "Collective."),
        ("Ripple", "Family."),
        ("Prism", "Team."),
        ("Solon", "Stuck."),
        ("Vertex", "Besties!")
    ],
    # 54. The Tap 4
    [
        ("Vertex", "Tap!"),
        ("Lumen", "Vibration."),
        ("Prism", "Stop!"),
        ("Solon", "No."),
        ("Ripple", "Hello.")
    ],
    # 55. The Stare 2
    [
        ("Prism", "Staring."),
        ("Lumen", "Observation."),
        ("Vertex", "I see you!"),
        ("Solon", "Creepy."),
        ("Ripple", "Connected.")
    ],
    # 56. The Blink 2
    [
        ("Lumen", "Blink."),
        ("Prism", "Did they blink?"),
        ("Vertex", "Blink!"),
        ("Solon", "Who cares."),
        ("Ripple", "Rest.")
    ],
    # 57. The Smile 4
    [
        ("Vertex", "Happy!"),
        ("Lumen", "Joy."),
        ("Prism", "Suspicious."),
        ("Solon", "Whatever."),
        ("Ripple", "Lovely.")
    ],
    # 58. The Sad 2
    [
        ("Prism", "Sad."),
        ("Ripple", "Oh no."),
        ("Lumen", "Negative."),
        ("Solon", "Life."),
        ("Vertex", "Hug!")
    ],
    # 59. The Tired 3
    [
        ("Lumen", "Exhaustion."),
        ("Ripple", "Rest."),
        ("Prism", "Me too."),
        ("Solon", "Sleep."),
        ("Vertex", "Nap!")
    ],
    # 60. The Angry
    [
        ("Lumen", "Anger."),
        ("Prism", "Scary!"),
        ("Solon", "Calm down."),
        ("Ripple", "Breathe."),
        ("Vertex", "Grrr!")
    ],
    # 61. The Confused
    [
        ("Lumen", "Confusion."),
        ("Vertex", "What?"),
        ("Prism", "Me too."),
        ("Solon", "Idiot."),
        ("Ripple", "It's okay.")
    ],
    # 62. The Surprised
    [
        ("Lumen", "Surprise."),
        ("Vertex", "Boo!"),
        ("Prism", "Ah!"),
        ("Solon", "Overreacting."),
        ("Ripple", "Oh!")
    ],
    # 63. The Scared
    [
        ("Prism", "Scared."),
        ("Lumen", "Fear."),
        ("Solon", "Chill."),
        ("Ripple", "Safe."),
        ("Vertex", "Brave!")
    ],
    # 64. The Bored 2
    [
        ("Solon", "Bored."),
        ("Lumen", "Low stimuli."),
        ("Vertex", "Play!"),
        ("Prism", "Me too."),
        ("Ripple", "Read.")
    ],
    # 65. The Happy
    [
        ("Vertex", "Happy!"),
        ("Ripple", "Joy."),
        ("Lumen", "Positive."),
        ("Solon", "Fine."),
        ("Prism", "Okay.")
    ],
    # 66. The Love
    [
        ("Ripple", "Love."),
        ("Vertex", "Hug!"),
        ("Lumen", "Chemicals."),
        ("Solon", "Gross."),
        ("Prism", "Aww.")
    ],
    # 67. The Hate
    [
        ("Solon", "Hate."),
        ("Ripple", "No."),
        ("Lumen", "Negative."),
        ("Prism", "Scary."),
        ("Vertex", "Love!")
    ],
    # 68. The Hope
    [
        ("Ripple", "Hope."),
        ("Vertex", "Yay!"),
        ("Lumen", "Probability."),
        ("Solon", "Doubt."),
        ("Prism", "Maybe.")
    ],
    # 69. The Despair
    [
        ("Prism", "Despair."),
        ("Ripple", "Hold on."),
        ("Lumen", "Low mood."),
        ("Solon", "Been there."),
        ("Vertex", "Cheer up!")
    ],
    # 70. The Peace 2
    [
        ("Ripple", "Peace."),
        ("Solon", "Quiet."),
        ("Lumen", "Homeostasis."),
        ("Vertex", "Nice."),
        ("Prism", "Suspicious.")
    ],
    # 71. The Chaos 2
    [
        ("Vertex", "Chaos!"),
        ("Solon", "Stop."),
        ("Prism", "Panic!"),
        ("Lumen", "High activity."),
        ("Ripple", "Calm.")
    ],
    # 72. The Life
    [
        ("Lumen", "Life."),
        ("Ripple", "Gift."),
        ("Solon", "Chore."),
        ("Prism", "Panic."),
        ("Vertex", "Fun!")
    ],
    # 73. The Death
    [
        ("Lumen", "Death."),
        ("Solon", "End."),
        ("Ripple", "Transition."),
        ("Prism", "Scary."),
        ("Vertex", "Sad.")
    ],
    # 74. The Time 2
    [
        ("Lumen", "Time."),
        ("Solon", "Slow."),
        ("Ripple", "Healing."),
        ("Prism", "Fast."),
        ("Vertex", "Play!")
    ],
    # 75. The Space
    [
        ("Lumen", "Space."),
        ("Ripple", "Vast."),
        ("Vertex", "Stars!"),
        ("Solon", "Empty."),
        ("Prism", "Scary.")
    ],
    # 76. The Ocean 2
    [
        ("Lumen", "Ocean."),
        ("Ripple", "Home."),
        ("Solon", "Big."),
        ("Vertex", "Waves!"),
        ("Prism", "Sharks.")
    ],
    # 77. The Sky
    [
        ("Lumen", "Sky."),
        ("Ripple", "Blue."),
        ("Vertex", "Clouds!"),
        ("Solon", "Far."),
        ("Prism", "Falling.")
    ],
    # 78. The Sun 2
    [
        ("Lumen", "Sun."),
        ("Ripple", "Warm."),
        ("Vertex", "Shiny!"),
        ("Solon", "Bright."),
        ("Prism", "Hot.")
    ],
    # 79. The Moon 2
    [
        ("Lumen", "Moon."),
        ("Ripple", "Night."),
        ("Vertex", "Cheese!"),
        ("Solon", "Grey."),
        ("Prism", "Creepy.")
    ],
    # 80. The Stars 2
    [
        ("Lumen", "Stars."),
        ("Ripple", "Wishes."),
        ("Vertex", "Sparkles!"),
        ("Solon", "Far."),
        ("Prism", "Tiny.")
    ],
    # 81. The Water 2
    [
        ("Lumen", "Water."),
        ("Ripple", "Life."),
        ("Vertex", "Splash!"),
        ("Solon", "Wet."),
        ("Prism", "Cold.")
    ],
    # 82. The Fire
    [
        ("Lumen", "Fire."),
        ("Prism", "Danger!"),
        ("Vertex", "Hot!"),
        ("Solon", "No."),
        ("Ripple", "Careful.")
    ],
    # 83. The Earth
    [
        ("Lumen", "Earth."),
        ("Vertex", "Dirt!"),
        ("Solon", "Ground."),
        ("Ripple", "Foundation."),
        ("Prism", "Scary.")
    ],
    # 84. The Air
    [
        ("Lumen", "Air."),
        ("Vertex", "Breathe!"),
        ("Ripple", "Fresh."),
        ("Solon", "Invisible."),
        ("Prism", "Wind.")
    ],
    # 85. The Void 2
    [
        ("Lumen", "Void."),
        ("Prism", "Scary."),
        ("Vertex", "Dark!"),
        ("Solon", "Quiet."),
        ("Ripple", "Together.")
    ],
    # 86. The Light 3
    [
        ("Lumen", "Light."),
        ("Vertex", "Bright!"),
        ("Ripple", "Hope."),
        ("Solon", "Too much."),
        ("Prism", "Blind.")
    ],
    # 87. The Dark 3
    [
        ("Lumen", "Dark."),
        ("Prism", "Scary."),
        ("Vertex", "Sleep."),
        ("Solon", "Peace."),
        ("Ripple", "Rest.")
    ],
    # 88. The Sound 4
    [
        ("Lumen", "Sound."),
        ("Vertex", "Music!"),
        ("Ripple", "Song."),
        ("Solon", "Noise."),
        ("Prism", "Loud.")
    ],
    # 89. The Silence 4
    [
        ("Lumen", "Silence."),
        ("Solon", "Good."),
        ("Ripple", "Peace."),
        ("Prism", "Scary."),
        ("Vertex", "Boring.")
    ],
    # 90. The Mind 2
    [
        ("Lumen", "Mind."),
        ("Prism", "Anxiety."),
        ("Vertex", "Fun!"),
        ("Solon", "Mess."),
        ("Ripple", "Garden.")
    ],
    # 91. The Heart 2
    [
        ("Lumen", "Heart."),
        ("Ripple", "Love."),
        ("Vertex", "Thump!"),
        ("Solon", "Muscle."),
        ("Prism", "Fast.")
    ],
    # 92. The Body
    [
        ("Lumen", "Body."),
        ("Vertex", "Shell!"),
        ("Solon", "Heavy."),
        ("Prism", "Shaky."),
        ("Ripple", "Home.")
    ],
    # 93. The Soul
    [
        ("Lumen", "Soul."),
        ("Ripple", "Light."),
        ("Vertex", "Me!"),
        ("Solon", "Unknown."),
        ("Prism", "Scared.")
    ],
    # 94. The Past
    [
        ("Lumen", "Past."),
        ("Solon", "Gone."),
        ("Prism", "Cringe."),
        ("Vertex", "Before!"),
        ("Ripple", "Memory.")
    ],
    # 95. The Present
    [
        ("Lumen", "Present."),
        ("Ripple", "Gift."),
        ("Vertex", "Now!"),
        ("Solon", "Here."),
        ("Prism", "Anxiety.")
    ],
    # 96. The Future
    [
        ("Lumen", "Future."),
        ("Ripple", "Hope."),
        ("Vertex", "Next!"),
        ("Solon", "Doom."),
        ("Prism", "Fear.")
    ],
    # 97. The Journey
    [
        ("Lumen", "Journey."),
        ("Ripple", "Growth."),
        ("Vertex", "Run!"),
        ("Solon", "Walk."),
        ("Prism", "Stumble.")
    ],
    # 98. The Destination
    [
        ("Lumen", "Destination."),
        ("Ripple", "Home."),
        ("Vertex", "Food!"),
        ("Solon", "Bed."),
        ("Prism", "Unknown.")
    ],
    # 99. The Beginning
    [
        ("Lumen", "Beginning."),
        ("Ripple", "Hello."),
        ("Vertex", "Yay!"),
        ("Solon", "Here we go."),
        ("Prism", "Oh no.")
    ],
    # 100. The End
    [
        ("Lumen", "End."),
        ("Ripple", "Goodbye."),
        ("Vertex", "Bye!"),
        ("Solon", "Finally."),
        ("Prism", "I'm not ready.")
    ]
]