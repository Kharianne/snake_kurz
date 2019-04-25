import pygame
import random

# Initializace pygame
pygame.init()

# Nahrani obrazku
gameover_pic = pygame.image.load("gameover.png")
# Pro obrázek hada si připravte čtvereček o požadované barvě velikosti 20x20 pixelů
snake_pic = pygame.image.load("snake.png")
# Zkuste se zamyslet, proc had ne vždy jablko sní
food_pic = pygame.image.load("appler.png")

# Nastartovani promennych
play = True
gameover = False
grow = False
# List do kterého budeme ukládat souřadnice, kde se objevily
food = []
# Úvodní směr pohybu hada - x, y - 1, 0 had se pohybuje doprava
direction = (1, 0)
speedup = 0
clock = pygame.time.Clock()

# Velikost, rychlost, pocatecni pozice
charsize = 20
sizex, sizey = 50, 50
# to je casovac, ktery dela pauzu mezi objevenim noveho jidla
step = 20
# Souřadnice hada
snake = [(i, sizey//2) for i in reversed(range(6))]
print(snake)
# Z printu vidíte, že list se souřadnicemi hada vypadá:
# [(5, 25), (4, 25), (3, 25), (2, 25), (1, 25), (0, 25)]
# Zkuste kod vysse nahradit uz pripravenym polem a overit si,
# ze se opravdu nic nezmenilo
# Co jeden par souradnic - to jedna pozice, kde se vykresli ctverecek hada

# Slovnik (dictionary - zkuste se kouknout na netu, co to presne je za strukturu)
# Ve slovniku jsou prirazene smery pohybu pro jednotlive stisknuti klavesy
DIRECTIONS = {
    pygame.K_RIGHT: (1, 0), # had se pohybuje vpravo, x se meni o 1
    pygame.K_UP: (0, -1), # had se pohybuje nahoru, y se meni o -1
    pygame.K_LEFT: (-1, 0), # had se pohybuje vlevo, x se meni o -1
    pygame.K_DOWN: (0, 1), # had se pohybuje dolu, y se meni o 1
}

# Vytvoreni obrazovky, na ktere se bude odehravat hra
screen = pygame.display.set_mode((sizex * charsize, sizey * charsize))

# Samotna hra
while play:
    # Klavesnicove vstupy uzivatele
    # Prochazime list se zaznamenanymi vstupy od uzivatele
    for event in pygame.event.get():
        # krizek
        if event.type == pygame.QUIT:
            play = False
        elif event.type == pygame.KEYDOWN:
            # escape
            if event.key == pygame.K_ESCAPE:
                play = False
            # sipky
            # podminka, ktera umoznuje to, ze kdyz zmackneme sipku doleva zatimco had bezi vpravo, aby hra neskoncila
            # zkuste se zamyslet cim, to je?
            # analogicky to funguje pro dalsi stavy
            if tuple(i*(-1) for i in DIRECTIONS[event.key]) == direction:
                continue
            # Pokud podminka vysse nebyla splnena, tak nastavime promennou direction na prislusnou hodnotu podle
            # stisknute klavesy (hodnoty se prectou ze slovniku DIRECTIONS
            direction = DIRECTIONS[event.key]

    # Posun hada
    # Na prvni pozici v listu s telem hada pridame novou souradnici, ktera odpovida smeru pohybu hada
    # Zmacknuti klavesy tedy nedela pohyb hada, ale urcuje v jakem smeru se vygeneruje nova souradnice pro hlavu =
    # prvni ctverecek
    snake.insert(0, tuple(map(sum, zip(snake[0], direction))))
    print(len(snake))
    print(snake)
    # Kdyz had nepapa, tak ani neroste proto musime odebrat posledni souradnici - to udela snake.pop()
    if not grow:
        snake.pop()
    # Pokud had zrovna jedl, tak souradnici neodebereme - had se tedy zvetsi, ale zaroven nastavime zpet promennou grow
    # na False, aby mohl v dalsim provedeni cyklu had jist
    else:
        grow = False

    # Krmeni
    # Postupne odcitame z casovace
    step -= 1
    # Pokud prvni souradnice hada je soucasne i jako souradnice v listu s jidlem, tak had i jidlo jsou na stejne pozici
    # Z toho vyplyva, ze had se jidla dotyka = jidlo sebral
    if snake[0] in food:
        # Po uspesnem snezeni zvysime rychlost hry
        speedup += 1
        # Odebereme jidlo z pole s jeho souradnicemi, jidlo uz je snedene, proto jej uz nevykreslujeme
        food.remove(snake[0])
        # Had se najedl, proto grow musi byt True, aby mohl vyrust
        grow = True
    # Pokud step klesne z puvodnich 20 na 0, tak zobrazime dalsi jidlo
    if step == 0:
        # Novemu jidlu priradime nahodne souradnice
        newfood = random.randrange(sizex), random.randrange(sizey)
        # Zkontrolujeme, jestli nahodou jidlo neni na pozici, kde je nejaka cast hada nebo uz na jeho pozici neni
        # jine jidlo
        # Pokud tomu tak neni, muzeme pridat souradnice noveho jidla do listu s jidlem
        if newfood not in snake and newfood not in food:
            food.append(newfood)
            # Znovu nastavime casovac pred objevenim noveho jidla na 20
            step = 20

    # Kontrola pozice
    # Kontrolujeme aby nam had neujel z hraci plochy
    if not 0 <= snake[0][0] < sizex or not 0 <= snake[0][1] < sizey:
        gameover = True
    if snake[0] in snake[1:]:
        gameover = True

    # Kresleni
    # V predchazejici casti cyklu jsme si pripravily veskere promenne, ktere potrebujeme k vykresleni hada:
    ## List se souradnicemi s telem hada
    ## List se souradnicemi s jidlem
    ## apod.
    if play:
        # vyplnime nasi hraci plochu cernou barvou (muzete zkusit experimentovat)
        screen.fill((0, 0, 0))
        if gameover:
            # Pokud bude konec hry, tak vykreslime na obrazovku GAME OVER obrazek
            screen.blit(gameover_pic, (0, 0))
        else:
            # V pripade, ze hra bezi generujeme na zaklade souradnic
            # Tento cyklus generuje vykresli na hraci plochu jidlo - na souradnice v listu
            for x, y in food:
                screen.blit(food_pic, (x * charsize, y * charsize))
            # Tento cyklus vykresli ctverecky hada na hraci plochu - podle souradnic v listu pro hada
            for x, y in snake:
                screen.blit(snake_pic, (x * charsize, y * charsize))
        pygame.display.update()

    # Casovani
    # Postupne hru zrychlujeme o promennou speedup
    # tick si muzete predstavit jako FPS
    clock.tick(5 + speedup)