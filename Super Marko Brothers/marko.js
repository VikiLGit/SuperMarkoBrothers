// ============================================================================
// Super Marko Brothers
// the original game with the original name and the definitely original code
// ============================================================================

const SIZE = 80;
const SCREEN_WIDTH = SIZE * 10;   // 800
const SCREEN_HEIGHT = SIZE * 7.5; // 600

// Luodaan peli-ikkuna (Canvas)
const canvas = document.createElement(`canvas`);
canvas.width = SCREEN_WIDTH;
canvas.height = SCREEN_HEIGHT;
document.body.appendChild(canvas);
const ctx = canvas.getContext(`2d`);
ctx.imageSmoothingEnabled = false;
ctx.mozImageSmoothingEnabled = false; // Vanhemmat Firefoxit
ctx.webkitImageSmoothingEnabled = false; // Vanhemmat Safarit/Chromet
ctx.msImageSmoothingEnabled = false; // Internet Explorer
// Globaalit muuttujat ja pelitilat
let jsonFile = null;
let is_running = true;
let run = true;
let lives = 3;
let level = 1;
let final_level = 1;
let score = 0;
let current_level_score = 0;
let food = 0;
let global_x_offset = 0;
let global_y_offset = 0;
let t_velocity = 9;
let x_delta = 0.91;
let gravity = 1.1 * (SIZE / 80);

let polo_murderer = false;
let marko_murderer = false;
let has_killed = false;
let touch = false;
let win = false;

// Listat objekteille
let entities = [];
let items = [];
let sand10x_list = [], sand_list = [], brick3x_list = [], brick_list = [];
let lootbox_taco_list = [], well_list = [], canopy_list = [];

// Peliobjektien tyypit
let sand10x, sand, brick3x, brick, lootbox_taco, well, canopy, bg;
let characters = []; // Sisältää: [polo_frames, marko_frames, doge_frames, car_frames]

// Loppukohtauksen resurssit
let prisonImg, blissImg, policerImg;

// High Score -muuttujat
let game_state = `GAMEPLAY`; // GAMEPLAY, GAMEOVER, ASK_SAVE, WRITING_NAME, SCOREBOARD
let high_scores = [];
let score_name = ``;
let scoreboard_scroll = 0;

// Äänet
const jump_sound = new Audio(`./resources/sound/jump.wav`);
jump_sound.volume = 0.01;
const taco_sound = new Audio(`./resources/sound/taco_sound.wav`);
taco_sound.volume = 0.01;
let current_music = null;

function playMusic(path, loop = true) {
    if (current_music) current_music.pause();
    current_music = new Audio(path);
    current_music.volume = 1;
    current_music.loop = loop;
    current_music.play().catch(() => {});
}

// Ohjaimet
const keys = {};
window.addEventListener(`keydown`, (e) => {
    const k = e.key;
    keys[k] = true;
    handleStateInput(e);
});
window.addEventListener(`keyup`, (e) => {
    keys[e.key] = false;
});

// Pelaajan attribuuttiluokka (Attribute)
class PlayerAttribute {
    constructor(y_velocity, x_velocity, on_ground, speed, characterType, x_pos, y_pos, can_jump, jump_time, jump, max_jump) {
        this.y_velocity = y_velocity;
        this.x_velocity = x_velocity;
        this.on_ground = Boolean(on_ground);
        this.speed = speed * (SIZE / 80);
        this.characterType = characterType; // 0: Polo, 1: Marko
        this.x_pos = x_pos;
        this.y_pos = y_pos;
        this.can_jump = Boolean(can_jump);
        this.jump_time = jump_time;
        this.jump = jump * (SIZE / 80);
        this.max_jump = max_jump;
        this.alive = true;
        this.frameid = 0;
        this.delay = 0;
        this.frame_count = 4;
        this.flip = false;
    }

    get rect() {
        return { x: this.x_pos, y: this.y_pos, width: SIZE, height: SIZE };
    }

    update_velocity(x_delta, gravity) {
        if (this.y_velocity > t_velocity * (SIZE / 80)) {
            this.y_velocity = t_velocity * (SIZE / 80);
        } else {
            this.y_velocity += gravity;
        }
        this.x_velocity = this.x_velocity * x_delta;
        this.x_pos += this.x_velocity;
        this.y_pos += this.y_velocity;
    }

    camera() {
        if (this.x_pos >= 400 * (SIZE / 80)) {
            this.x_pos = (400 * (SIZE / 80)) - 1;
            if (this.x_velocity > 0) global_x_offset -= this.x_velocity;
            else global_x_offset += this.x_velocity;
        }
        if (this.y_pos <= 50 * (SIZE / 80)) {
            this.y_pos = (50 * (SIZE / 80)) - 1;
            global_y_offset -= this.y_velocity;
        }
        if (this.y_pos >= 50 * (SIZE / 80) && !(global_y_offset < 1 * (SIZE / 80))) {
            this.y_pos = 50 * (SIZE / 80);
            global_y_offset -= this.y_velocity;
        }
        if (global_y_offset <= 0) global_y_offset = 0;
        if (this.x_pos <= 0) {
            this.x_pos = 0;
            this.x_velocity = 0;
        }
        if (this.x_pos >= SIZE * 10) this.x_pos = (SIZE * 10) - 1;
    }

    movement() {
        this.delay += 1;
        if (this.delay === 6) {
            this.frameid += 1;
            this.delay = 0;
            if (this.frameid >= this.frame_count) this.frameid = 0;
        }

        if (keys[`l`] || keys[`L`]) {
            console.log((this.x_pos - global_x_offset), (this.y_pos - global_y_offset));
            console.log(Math.floor((this.x_pos - global_x_offset) / 80), Math.floor((this.y_pos - global_y_offset) / 80));
        }

        if (this.on_ground) {
            this.can_jump = true;
            this.jump_time = 0;
        } else if (this.jump_time > 0 && this.jump_time < this.max_jump) {
            this.can_jump = true;
        } else {
            this.on_ground = false;
            this.can_jump = false;
        }

        let currentFrameImg;
        let pFrames = characters[this.characterType];

        // Hyppy- ja kävelyanimaatioiden piirtolokiikka täsmälleen alkuperäisestä koodista
        if ((keys[`w`] || keys[`W`]) && this.can_jump) {
            this.y_velocity = this.jump;
            this.jump_time += 1;
            try { jump_sound.currentTime = 0; jump_sound.play(); } catch(e){}

            if ((keys[`a`] || keys[`A`]) && (keys[`d`] || keys[`D`])) {
                currentFrameImg = pFrames[5];
            } else if (keys[`a`] || keys[`A`]) {
                this.flip = true;
                this.x_velocity -= this.speed;
                currentFrameImg = pFrames[5];
            } else if (keys[`d`] || keys[`D`]) {
                this.flip = false;
                this.x_velocity += this.speed;
                currentFrameImg = pFrames[5];
            } else {
                currentFrameImg = pFrames[5];
            }
        } else if (this.jump_time > 0 && this.can_jump) {
            this.jump_time += this.max_jump + 100;
            currentFrameImg = pFrames[5];
        } else if ((keys[`a`] || keys[`A`]) && (keys[`d`] || keys[`D`])) {
            currentFrameImg = pFrames[0];
        } else if (keys[`a`] || keys[`A`]) {
            this.flip = true;
            this.x_velocity -= this.speed;
            currentFrameImg = pFrames[this.frameid];
        } else if (keys[`d`] || keys[`D`]) {
            this.flip = false;
            this.x_velocity += this.speed;
            currentFrameImg = pFrames[this.frameid];
        } else {
            currentFrameImg = pFrames[0];
        }

        // Renderöidään pelaaja kankaalle (Canvas) flippaus huomioiden
        ctx.save();
        if (this.flip) {
            ctx.scale(-1, 1);
            ctx.drawImage(currentFrameImg, -(this.x_pos + SIZE), this.y_pos, SIZE, SIZE);
        } else {
            ctx.drawImage(currentFrameImg, this.x_pos, this.y_pos, SIZE, SIZE);
        }
        ctx.restore();
    }
}

let player = null;

// Pelin kiinteät objektit (Object)
class GameObject {
    constructor(width, height, img, loot = null, collision = true) {
        this.width = width;
        this.height = height;
        this.loot = loot;
        this.texture = img;
        this.collision = collision;
    }

    draw(lista, entitiesList = null) {
        for (let location of lista) {
            ctx.drawImage(this.texture, global_x_offset + location[0], global_y_offset + location[1], this.width, this.height);
            
            if (player && player.alive && this.collision) {
                let px = player.x_pos - global_x_offset;
                let py = player.y_pos - global_y_offset;

                // Osumat palikan päällä
                if ((location[1] < py + SIZE && py + SIZE < location[1] + (SIZE / 4)) && 
                    (location[0] - SIZE + (SIZE / 8) < px && px < location[0] + this.width - (SIZE / 8))) {
                    player.y_pos = global_y_offset + location[1] - this.height;
                    player.y_velocity = 0;
                    player.on_ground = true;
                    touch = true;
                }
                // Osumat palikan alla
                if ((location[1] + this.height >= py && py >= location[1] + this.height - (SIZE / 4)) && 
                    (location[0] - SIZE + (SIZE / 8) <= px && px <= location[0] + this.width - (SIZE / 8))) {
                    player.y_pos = global_y_offset + location[1] + this.height;
                    player.y_velocity = 0;
                    if (this.loot !== 0 && this.loot !== null) {
                        items.push(new Item(this.loot, location[0], location[1] - SIZE));
                        this.loot = 0;
                    }
                }
                // Osumat palikan oikea laita
                if ((location[0] <= px + SIZE && px + SIZE <= location[0] + (SIZE / 4)) && 
                    (location[1] + (SIZE / 8) <= py + SIZE && py + SIZE <= location[1] + this.height + SIZE - (SIZE / 8))) {
                    player.x_pos = global_x_offset + location[0] - SIZE;
                }
                // Osumat palikan vasen laita
                if ((location[0] + this.width >= px && px >= location[0] - (SIZE / 4)) && 
                    (location[1] + (SIZE / 8) <= py + SIZE && py + SIZE <= location[1] + this.height + SIZE - (SIZE / 8))) {
                    player.x_pos = global_x_offset + location[0] + this.width;
                }
            }

            if (entitiesList) {
                for (let entity of entitiesList) {
                    // NPC osumat palikoihin

if ((location[1] < entity.y_pos + SIZE && entity.y_pos + SIZE < location[1] + (SIZE / 4)) && (location[0] - SIZE < entity.x_pos && entity.x_pos < location[0] + this.width)) {
entity.y_pos = location[1] - this.height;
entity.y_velocity = 0;
}
if ((location[1] + this.height >= entity.y_pos && entity.y_pos >= location[1] + this.height - (SIZE / 4)) && (location[0] - SIZE <= entity.x_pos && entity.x_pos <= location[0] + this.width)) {
entity.y_pos = location[1] + this.height;
}
if ((location[0] <= entity.x_pos + SIZE && entity.x_pos + SIZE <= location[0] + (SIZE / 4)) && (location[1] + (SIZE / 8) <= entity.y_pos + SIZE && entity.y_pos + SIZE <= location[1] + this.height + SIZE - (SIZE / 8))) {
entity.x_pos = location[0] - SIZE;
if (entity.x_velocity > 0) entity.x_velocity = -entity.x_velocity;
}
if ((location[0] + this.width >= entity.x_pos && entity.x_pos >= location[0] - (SIZE / 4)) && (location[1] + (SIZE / 8) <= entity.y_pos + SIZE && entity.y_pos + SIZE <= location[1] + this.height + SIZE - (SIZE / 8))) {
entity.x_pos = location[0] + this.width;
if (entity.x_velocity < 0) entity.x_velocity = -entity.x_velocity;
}
}
}
}
}
}
// Vihollisluokka (Enemy)
class Enemy {
constructor(y_velocity, x_velocity, x_pos, y_pos, frame_count, anim_speed, type, character) {
this.y_velocity = y_velocity;
this.x_velocity = x_velocity * (SIZE / 80);
this.x_pos = x_pos;
this.y_pos = y_pos;
this.frameid = 0;
this.delay = 0;
this.anim_speed = anim_speed;
this.frame_count = frame_count;
this.characterIdx = character === 0 ? 3 : 2; // 3: Car, 2: Doge
this.type = type;
this.flip = false;
}
get rect() {
return {
x: this.x_pos + (SIZE / 8) + global_x_offset,
y: this.y_pos + global_y_offset + (SIZE / 8),
width: SIZE * 0.75,
height: SIZE * 0.75
};
}
update(gravity) {
if (this.y_velocity > t_velocity * (SIZE / 80)) this.y_velocity = t_velocity * (SIZE / 80);
else this.y_velocity += gravity * (SIZE / 80);
this.x_pos += this.x_velocity;
this.y_pos += this.y_velocity;
this.delay += 1;
if (this.delay === this.anim_speed) {
this.frameid += 1;
this.delay = 0;
if (this.frameid >= this.frame_count) this.frameid = 0;
}
let img = characters[this.characterIdx][this.frameid];
ctx.save();
let drawX = this.x_pos + global_x_offset;
let drawY = this.y_pos + global_y_offset;
if (this.x_velocity <= 0) {
ctx.translate(drawX, drawY);
if (this.flip) { ctx.scale(1, -1); ctx.drawImage(img, 0, -SIZE, SIZE, SIZE); }
else { ctx.drawImage(img, 0, 0, SIZE, SIZE); }
} else {
ctx.translate(drawX + SIZE, drawY);
ctx.scale(-1, 1);
if (this.flip) { ctx.scale(1, -1); ctx.drawImage(img, 0, -SIZE, SIZE, SIZE); }
else { ctx.drawImage(img, 0, 0, SIZE, SIZE); }
}
ctx.restore();
}
}
// Esine-luokka (Item)
class Item {
constructor(type, x_pos, y_pos) {
this.type = type;
this.x_pos = x_pos;
this.y_pos = y_pos;
this.texture = new Image();
if (type === 1) this.texture.src = `./resources/textures/items/taco.png`;
else if (type === 2) this.texture.src = `./resources/textures/items/sauce.png`;
else if (type === 3) this.texture.src = `./resources/textures/items/bucket.png`;
else this.texture.src = `./resources/textures/items/taco.png`;
}
get rect() {
return { x: this.x_pos + global_x_offset, y: this.y_pos + global_y_offset, width: SIZE, height: SIZE };
}
draw() {
ctx.drawImage(this.texture, this.x_pos + global_x_offset, this.y_pos + global_y_offset, SIZE, SIZE);
}
}
function rectCollide(r1, r2) {
return r1.x < r2.x + r2.width && r1.x + r1.width > r2.x && r1.y < r2.y + r2.height && r1.y + r1.height > r2.y;
}
// Kenttien tietojen lataaja JSON:sta
function loader(lvlNum) {
let lvlData = jsonFile[`levels`][lvlNum - 1];
sand10x_list = []; sand_list = []; brick3x_list = []; brick_list = [];
lootbox_taco_list = []; well_list = []; canopy_list = [];
// Alustat
for (let key in lvlData[`platforms`]) {
for (let loc of lvlData[`platforms`][key]) {
if (typeof loc.x === `number` && typeof loc.y === `number`) {
let coords = [loc.x * SIZE, loc.y * SIZE];
if (key === `sand10x`) sand10x_list.push(coords);
else if (key === `sand`) sand_list.push(coords);
else if (key === `brick3x`) brick3x_list.push(coords);
else if (key === `brick`) brick_list.push(coords);
else if (key === `lootbox_taco`) lootbox_taco_list.push(coords);
else if (key === `well`) well_list.push(coords);
else if (key === `canopy`) canopy_list.push(coords);
}
}
}
// Viholliset
entities = [];
for (let e of lvlData[`entities`]) {
entities.push(new Enemy(e.y_velocity, e.x_velocity, e.x * SIZE, e.y * SIZE, e.frame_count, e.anim_speed, e.type, e.character));
}
// Esineet
items = [];
for (let i of lvlData[`items`]) {
items.push(new Item(i.type, i.x * SIZE, i.y * SIZE));
}
// Erityisattribuutit (Misc)
let misc = lvlData[`misc`];
if (misc.food !== undefined) food = misc.food;
if (misc.music !== undefined) playMusic(`./resources/${misc.music}`);
if (misc.playerAttribute) {
let p = misc.playerAttribute;
player = new PlayerAttribute(p.y_velocity, p.x_velocity, p.on_ground, p.speed, p.character, p.x_pos * SIZE, p.y_pos * SIZE, p.can_jump, p.jump_time, p.jump, p.max_jump);
}
const loadObj = (data) => {
let img = new Image(); img.src = `./resources/${data.texture}`;
return new GameObject(data.width * SIZE, data.height * SIZE, img, data.loot, Boolean(data.collision));
};
if (misc.sand10x) sand10x = loadObj(misc.sand10x);
if (misc.sand) sand = loadObj(misc.sand);
if (misc.brick) brick = loadObj(misc.brick);
if (misc.brick3x) brick3x = loadObj(misc.brick3x);
if (misc.lootbox_taco) lootbox_taco = loadObj(misc.lootbox_taco);
if (misc.well) well = loadObj(misc.well);
if (misc.canopy) canopy = loadObj(misc.canopy);
if (misc.bg_colour) bg_colour = misc.bg_colour;
if (misc.bg) {
bg = new Image();
bg.src = `./resources/${misc.bg.texture}`;
}
}
// Drawer hoitaa osumatunnistukset ja renderöinnin pyynnöt
function drawer() {
let collect = [];
for (let item of items) {
if (player && rectCollide(item.rect, player.rect)) {
collect.push(item);
if (item.type === 3) win = true;
else if (item.type === 1) {
try { taco_sound.play(); } catch(e){}
food += 1000;
lives += 1;
} else if (item.type === 2) {
lives += 1;
}
}
}
items = items.filter(i => !collect.includes(i));
for (let item of items) {
if (item.x_pos <= -global_x_offset + (SIZE * 10)) item.draw();
}
let ded = [];
for (let entity of entities) {
if (entity.y_pos >= SIZE * 8.75) ded.push(entity);
let pRect = player ? player.rect : null;
if (entity.type === 1 && pRect) {
let ex = entity.x_pos + global_x_offset;
let ey = entity.y_pos + global_y_offset;
if ((ex + (SIZE / 16) <= player.x_pos + SIZE && player.x_pos + SIZE <= ex + (SIZE * 2) - (SIZE / 16)) &&
(ey - SIZE - (SIZE / 4) <= player.y_pos && player.y_pos <= ey - SIZE) && (player.y_velocity > 0)) {
ded.push(entity);
player.y_velocity = player.jump;
current_level_score += 100;
has_killed = true;
} else if (rectCollide(entity.rect, pRect)) {
player.alive = false;
}
} else if (entity.type === 0 && pRect) {
let ex = entity.x_pos + global_x_offset;
let ey = entity.y_pos + global_y_offset;
if ((ex + (SIZE / 8) <= player.x_pos + SIZE && player.x_pos + SIZE <= ex + (SIZE * 2) - (SIZE / 8)) &&
(ey - SIZE - (SIZE / 4) <= player.y_pos && player.y_pos <= ey - SIZE) && (player.y_velocity > 0)) {
player.y_velocity = player.jump;
if (!entity.flip) {
entity.flip = true;
current_level_score += 100;
entity.x_velocity *= 10;
} else {
entity.x_velocity = -entity.x_velocity;
}
has_killed = true;
} else if (rectCollide(entity.rect, pRect) && player.alive) {
player.alive = false;
}
}
for (let upsidedown of entities) {
if (upsidedown.flip && upsidedown !== entity) {
if (rectCollide(entity.rect, upsidedown.rect)) {
if (entity.flip) { ded.push(upsidedown); current_level_score += 100; }
ded.push(entity); current_level_score += 100;
}
}
}
}
entities = entities.filter(e => !ded.includes(e));
for (let entity of entities) {
if (entity.x_pos < -global_x_offset + (SIZE * 12.5)) entity.update(gravity);
}
if (level >= 1 && level <= final_level) {
touch = false;
if (sand10x) sand10x.draw(sand10x_list, entities);
if (sand) sand.draw(sand_list, entities);
if (brick3x) brick3x.draw(brick3x_list, entities);
if (brick) brick.draw(brick_list, entities);
if (lootbox_taco) lootbox_taco.draw(lootbox_taco_list, entities);
if (well) well.draw(well_list, entities);
if (canopy) canopy.draw(canopy_list, entities);
if (!touch && player) player.on_ground = false;
}
}
function hud() {
ctx.fillStyle = `rgb(0,0,0)`;
ctx.font = `bold ${SIZE * 0.4}px sans-serif`;
ctx.fillText(`lives`, SIZE * 8.125, 25);
ctx.fillText(`${lives}`, SIZE * 8.75, 55);
ctx.fillText(`food`, SIZE * 3.125, 25);
ctx.fillText(`${Math.floor(food / 10)}`, SIZE * 3.5, 55);
ctx.fillText(`level`, SIZE * 5.625, 25);
ctx.fillText(`${level}`, SIZE * 6.25, 55);
ctx.fillText(`score`, SIZE * 0.625, 25);
ctx.fillText(`${Math.floor(score + current_level_score)}`, SIZE * 1.25, 55);
}
// Korvataan Pythonin CSV tallentamalla tiedot selaimen LocalStorageen
function saveScoreToLocalStorage(name, finalScore) {
let scores = JSON.parse(localStorage.getItem(`SuperMarkoBrothers_Scores`)) || [];
scores.push({ name: name, score: parseInt(finalScore) });
scores.sort((a, b) => b.score - a.score);
localStorage.setItem(`SuperMarkoBrothers_Scores`, JSON.stringify(scores));
loadHighScores();
}
function loadHighScores() {
let scores = JSON.parse(localStorage.getItem(`SuperMarkoBrothers_Scores`)) || [];
high_scores = scores.map(s => [s.name, String(s.score)]);
while (high_scores.length < 12) {
high_scores.push([``, ``]);
}
}
function drawScoreboard() {
ctx.fillStyle = `rgb(0,0,0)`;
ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
ctx.fillStyle = `rgb(255,255,255)`;
ctx.font = `${SIZE * 0.4}px sans-serif`;
for (let i = 0; i < 12; i++) {
let idx = scoreboard_scroll + i;
if (idx < high_scores.length) {
ctx.fillText(`${idx + 1}`, 10, i * 50 + 40);
ctx.fillText(high_scores[idx][0], 100, i * 50 + 40);
ctx.fillText(high_scores[idx][1], 400, i * 50 + 40);
}
}
}
// Käsitellään tilansiirtymät ja tekstinsyöttö
function handleStateInput(e) {
if (game_state === `ASK_SAVE`) {
if (e.key === `Enter`) {
game_state = `WRITING_NAME`;
score_name = ``;
} else if (e.key === `Escape`) {
loadHighScores();
game_state = `SCOREBOARD`;
}
} else if (game_state === `WRITING_NAME`) {
if (e.key === `Backspace`) {
score_name = score_name.slice(0, -1);
} else if (e.key === `Escape` || e.key === `Enter`) {
saveScoreToLocalStorage(score_name, score);
game_state = `SCOREBOARD`;
} else if (score_name.length < 8 && e.key.length === 1 && e.key !== `\t`) {
score_name += e.key;
}
} else if (game_state === `SCOREBOARD`) {
if (e.key === `ArrowDown` && scoreboard_scroll + 12 < high_scores.length) {
scoreboard_scroll++;
} else if (e.key === `ArrowUp` && scoreboard_scroll > 0) {
scoreboard_scroll--;
} else if (e.key === `Escape`) {
// Palautetaan alkutilaan
is_running = false;
window.location.reload();
}
}
}
// Pelaajan kuolinanimaatio-looppi
function runPlayerDeathAnimation(callback) {
lives -= 1;
run = false;
if (player) { player.x_velocity = 0; player.y_velocity = 0; }
playMusic((level === 1 || level === 3) ? `./resources/sound/deadin1.wav` : `./resources/sound/deadin2.wav`, false);
let frameCount = 0;
function deathLoop() {
ctx.fillStyle = `rgb(0,0,0)`;
ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
if (bg) ctx.drawImage(bg, global_x_offset, global_y_offset, SIZE * 100, SIZE * 7.5);
if (player) {
player.y_pos += player.y_velocity;
if (frameCount < 20) player.y_velocity = -10;
else player.y_velocity += 1;
}
drawer();
if (player) ctx.drawImage(characters[player.characterType][6], player.x_pos, player.y_pos, SIZE, SIZE);
frameCount++;
if (frameCount < 120) {
requestAnimationFrame(deathLoop);
} else {
callback();
}
}
requestAnimationFrame(deathLoop);
}
// Tason läpäisyanimaatio
function runLevelWinAnimation(callback) {
if (player) {
if (player.characterType === 0 && has_killed) polo_murderer = true;
if (player.characterType === 1 && has_killed) marko_murderer = true;
}
current_level_score += Math.floor(food / 10) * 10;
score += current_level_score;
playMusic(`./resources/sound/winnin.wav`, false);
let flippera = false, flipperb = false;
let frameCount = 0;
function winLoop() {
ctx.fillStyle = `rgb(${bg_colour.r || 0}, ${bg_colour.g || 0}, ${bg_colour.b || 0})`;
ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
if (bg) ctx.drawImage(bg, global_x_offset, global_y_offset, SIZE * 100, SIZE * 7.5);
ctx.save();
if (player) {
if (flippera) ctx.scale(-1, 1);
if (flipperb) ctx.scale(1, -1);
let dx = flippera ? -(player.x_pos + SIZE) : player.x_pos;
let dy = flipperb ? -(player.y_pos + SIZE) : player.y_pos;
ctx.drawImage(characters[player.characterType][0], dx, dy, SIZE, SIZE);
}
ctx.restore();
drawer();
// Alkuperäinen Python-flippauslogiikka animointiin
if (!flippera && flipperb) flipperb = false;
else if (flippera && flipperb) flippera = false;
else if (flippera && !flipperb) flipperb = true;
else if (!flippera && !flipperb) flippera = true;
frameCount++;
if (frameCount < 30) {
setTimeout(() => requestAnimationFrame(winLoop), 1000 / 15); // Lukittu 15 FPS:ään
} else {
level += 1;
callback();
}
}
requestAnimationFrame(winLoop);
}
// Loppukohtaus, kun kaikki tasot on pelattu läpi
function runEndGameCutscene() {
run = false;
let frameCount = 0;
function cutsceneLoop() {
ctx.fillStyle = `rgb(0,0,0)`;
ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
if (marko_murderer && polo_murderer) {
ctx.drawImage(prisonImg, 0, 0, SIZE * 10, SIZE * 7.5);
ctx.drawImage(policerImg, SIZE, SIZE * 6.25, SIZE, SIZE);
ctx.drawImage(policerImg, SIZE * 2.5, SIZE * 6.25, SIZE, SIZE);
ctx.drawImage(policerImg, SIZE * 3.75, SIZE * 6.25, SIZE, SIZE);
ctx.drawImage(characters[0][4], SIZE * 6.25, SIZE * 6.25, SIZE, SIZE);
ctx.drawImage(characters[1][4], SIZE * 6, SIZE * 6, SIZE, SIZE);
} else if (marko_murderer) {
ctx.drawImage(prisonImg, 0, 0, SIZE * 10, SIZE * 7.5);
ctx.drawImage(policerImg, SIZE, SIZE * 6.25, SIZE, SIZE);
ctx.drawImage(policerImg, SIZE * 2.5, SIZE * 6.25, SIZE, SIZE);
ctx.drawImage(policerImg, SIZE * 3.75, SIZE * 6.25, SIZE, SIZE);
ctx.drawImage(characters[1][4], SIZE * 6.25, SIZE * 6.25, SIZE, SIZE);
} else if (polo_murderer) {
ctx.drawImage(prisonImg, 0, 0, SIZE * 10, SIZE * 7.5);
ctx.drawImage(policerImg, SIZE, SIZE * 6.25, SIZE, SIZE);
ctx.drawImage(policerImg, SIZE * 2.5, SIZE * 6.25, SIZE, SIZE);
ctx.drawImage(policerImg, SIZE * 3.75, SIZE * 6.25, SIZE, SIZE);
ctx.drawImage(characters[0][4], SIZE * 6.25, SIZE * 6.25, SIZE, SIZE);
} else {
ctx.drawImage(blissImg, 0, 0, SIZE * 10, SIZE * 7.5);
ctx.drawImage(characters[1][4], SIZE * 1.75, SIZE * 3, SIZE, SIZE);
ctx.drawImage(characters[0][0], SIZE * 6.25, SIZE * 6.25, SIZE, SIZE);
}
frameCount++;
if (frameCount < 120) {
requestAnimationFrame(cutsceneLoop);
} else {
is_running = false;
lives = 0;
handleGameOverState();
}
}
requestAnimationFrame(cutsceneLoop);
}
function handleGameOverState() {
game_state = `GAMEOVER`;
playMusic(`./resources/sound/background_music_best.wav`, true);
ctx.fillStyle = `rgb(0,0,0)`;
ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
ctx.fillStyle = `rgb(255,255,255)`;
ctx.font = `${SIZE * 1.25}px sans-serif`;
ctx.fillText(`GAME OVER`, SIZE, SIZE * 3.125);
setTimeout(() => {
game_state = `ASK_SAVE`;
}, 1000);
}
// Pelisilmukka (Main loop)
function gameLoop() {
if (!is_running) {
// High score -tilojen renderöinti pelin sulkeuduttua
if (game_state === `ASK_SAVE`) {
ctx.fillStyle = `rgb(0,0,0)`;
ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
ctx.fillStyle = `rgb(255,255,255)`;
ctx.font = `${SIZE * 0.4}px sans-serif`;
ctx.fillText(`press enter to save score`, SIZE, SIZE * 3.125);
ctx.fillText(`press esc to continue without saving`, SIZE, SIZE * 3.5);
} else if (game_state === `WRITING_NAME`) {
ctx.fillStyle = `rgb(0,0,0)`;
ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
ctx.fillStyle = `rgb(255,255,255)`;
ctx.font = `${SIZE*0.4}px, sans-serif`;
ctx.fillText(`Enter Your Name Below. max 8 characters.`, 10, 30);
ctx.fillText(`(press esc to stop)`, 10, SIZE * 0.375 + 30);
ctx.font = `${SIZE * 1.25}px sans-serif`;
ctx.fillText(score_name, SIZE, SIZE * 3.125);
} else if (game_state === `SCOREBOARD`) {
drawScoreboard();
}
requestAnimationFrame(gameLoop);
return;
}
if (lives <= 0) {
score = Math.floor(current_level_score + score);
is_running = false;
handleGameOverState();
requestAnimationFrame(gameLoop);
return;
}
if (run) {
food -= 1;
ctx.fillStyle = `rgb(${bg_colour.r || 0}, ${bg_colour.g || 0}, ${bg_colour.b || 0})`;
ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
if (bg) ctx.drawImage(bg, global_x_offset, global_y_offset, SIZE * 100, SIZE * 7.5);
if (global_x_offset <= (SIZE * -90)) global_x_offset = (SIZE * -90);
if (player) {
player.update_velocity(x_delta, gravity);
drawer();
player.camera();
player.movement();
if (!player.alive) {
runPlayerDeathAnimation(() => {
run = true;
if (player) player.alive = true;
loader(level);
});
}
}
if (win) {
runLevelWinAnimation(() => {
win = false;
run = true;
if (level <= final_level) loader(level);
else runEndGameCutscene();
});
}
// Putoamiskuolema tai ruuan loppuminen
if (player && ((player.y_pos > (SIZE * 8.75) + global_y_offset && player.alive) || food <= 0)) {
runPlayerDeathAnimation(() => {
run = true;
if (player) player.alive = true;
loader(level);
});
}
hud();
}
requestAnimationFrame(gameLoop);
}
// Apufunktio ruutujen esilataukseen
function loadFramesArray(pathPattern, count) {
let arr = [];
for (let i = 1; i <= count; i++) {
let img = new Image();
img.src = pathPattern.replace(`{}`, i);
arr.push(img);
}
return arr;
}
// Alustus, joka odottaa sos.json-tiedostoa
async function init() {
const res = await fetch(`sos.json`);
jsonFile = await res.json();
try { final_level = jsonFile[`misc`][`levels`]; } catch(e) { final_level = 1; }
// Ladataan hahmojen spritet taulukkoon täsmälleen Python-indekseillä:
// characters[0]: Polo, characters[1]: Marko, characters[2]: Doge, characters[3]: Car
characters.push(loadFramesArray(`./resources/textures/Polo/Polo{}.png`, 7));
characters.push(loadFramesArray(`./resources/textures/marko/marko{}.png`, 7));
characters.push(loadFramesArray(`./resources/textures/doge/doge{}.png`, 2));
characters.push(loadFramesArray(`./resources/textures/car/car{}.png`, 6));
// Loppukohtauksen kuvat
prisonImg = new Image(); prisonImg.src = `./resources/textures/materials/background_prison.png`;
blissImg = new Image(); blissImg.src = `./resources/textures/materials/background_bliss.png`;
policerImg = new Image(); policerImg.src = `./resources/textures/police/policer.png`;
has_killed = false;
if (level <= final_level) loader(level);
requestAnimationFrame(gameLoop);
}
window.onload = init;