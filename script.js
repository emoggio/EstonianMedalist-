// Track previous medal state for snowflake trigger
let previousTotalMedals = 0;

// Load and display Olympic data
async function loadData() {
    try {
        const response = await fetch('data.json');
        const data = await response.json();

        const currentTotal = data.medals.gold + data.medals.silver + data.medals.bronze;

        updateMedalAnswer(data.medals, currentTotal);
        updateMedalCounter(data.medals);
        updateCompletedEvents(data.completed);
        updateUpcomingEvents(data.upcoming);

        // Trigger snowflakes if we just got our first medal or new medals
        if (currentTotal > previousTotalMedals && currentTotal > 0) {
            triggerSnowflakes();
        }

        // Start or stop continuous snowflakes based on medal status
        if (currentTotal > 0) {
            startContinuousSnowflakes();
        } else {
            stopContinuousSnowflakes();
        }

        previousTotalMedals = currentTotal;
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Update the main Yes/No answer
function updateMedalAnswer(medals, totalMedals) {
    const answerElement = document.getElementById('answer');

    if (totalMedals > 0) {
        answerElement.textContent = 'Yes';
        answerElement.className = 'answer yes';
    } else {
        answerElement.textContent = 'No';
        answerElement.className = 'answer no';
    }
}

// Update medal counter
function updateMedalCounter(medals) {
    document.getElementById('goldCount').textContent = medals.gold;
    document.getElementById('silverCount').textContent = medals.silver;
    document.getElementById('bronzeCount').textContent = medals.bronze;
}

// Update completed events list
function updateCompletedEvents(athletes) {
    const listElement = document.getElementById('completedList');

    if (!athletes || athletes.length === 0) {
        listElement.innerHTML = '<p class="empty-message">No completed events yet</p>';
        return;
    }

    listElement.innerHTML = athletes.map(athlete => `
        <div class="athlete-card ${athlete.medal ? athlete.medal : ''}">
            <div class="athlete-name">
                ${athlete.name}
                ${athlete.medal ? `<span class="medal-badge">${getMedalEmoji(athlete.medal)}</span>` : ''}
            </div>
            <div class="athlete-sport">${athlete.sport}</div>
            ${athlete.result ? `<div class="athlete-result">${athlete.result}</div>` : ''}
        </div>
    `).join('');
}

// Update upcoming events list
function updateUpcomingEvents(athletes) {
    const listElement = document.getElementById('upcomingList');

    if (!athletes || athletes.length === 0) {
        listElement.innerHTML = '<p class="empty-message">No upcoming events</p>';
        return;
    }

    listElement.innerHTML = athletes.map(athlete => `
        <div class="athlete-card">
            <div class="athlete-name">${athlete.name}</div>
            <div class="athlete-sport">${athlete.sport}</div>
            ${athlete.datetime ? `<div class="athlete-datetime">📅 ${athlete.datetime}</div>` : ''}
        </div>
    `).join('');
}

// Get medal emoji
function getMedalEmoji(medal) {
    const medals = {
        'gold': '🥇',
        'silver': '🥈',
        'bronze': '🥉'
    };
    return medals[medal] || '';
}

// Create a single snowflake
function createSnowflake() {
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');
    snowflake.textContent = ['❄', '❅', '❆'][Math.floor(Math.random() * 3)];

    // Random starting position
    snowflake.style.left = Math.random() * 100 + 'vw';

    // Random size
    const size = Math.random() * 1 + 0.5; // 0.5 to 1.5
    snowflake.style.fontSize = size + 'rem';

    // Random animation duration
    const duration = Math.random() * 3 + 4; // 4 to 7 seconds
    snowflake.style.animationDuration = duration + 's';

    document.body.appendChild(snowflake);

    // Remove snowflake after animation completes
    setTimeout(() => {
        snowflake.remove();
    }, duration * 1000);
}

// Trigger snowflake effect
function triggerSnowflakes() {
    // Create 50 snowflakes over 3 seconds
    const totalSnowflakes = 50;
    const duration = 3000; // 3 seconds

    for (let i = 0; i < totalSnowflakes; i++) {
        setTimeout(() => {
            createSnowflake();
        }, (duration / totalSnowflakes) * i);
    }
}

// Continuous snowflake effect when medals exist
let snowflakeInterval = null;
let snowPileHeight = 0;
const MAX_PILE_HEIGHT = 120; // Maximum pile height in pixels

function startContinuousSnowflakes() {
    // Don't start if already running
    if (snowflakeInterval) return;

    // Reset pile height when starting
    snowPileHeight = 0;
    updateSnowPile();

    // Create a snowflake every 200ms continuously
    snowflakeInterval = setInterval(() => {
        createSnowflake();

        // Gradually increase pile height (slower accumulation)
        if (snowPileHeight < MAX_PILE_HEIGHT) {
            snowPileHeight += 0.3; // Grow by 0.3px per snowflake
            updateSnowPile();
        }
    }, 200);
}

function stopContinuousSnowflakes() {
    if (snowflakeInterval) {
        clearInterval(snowflakeInterval);
        snowflakeInterval = null;
    }

    // Slowly melt the pile
    const meltInterval = setInterval(() => {
        if (snowPileHeight > 0) {
            snowPileHeight -= 2;
            updateSnowPile();
        } else {
            clearInterval(meltInterval);
        }
    }, 50);
}

function updateSnowPile() {
    const pileElement = document.getElementById('snowPile');
    if (pileElement) {
        pileElement.style.height = `${Math.max(0, snowPileHeight)}px`;
    }
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', () => {
    loadData();

    // Check on initial load if we have medals to show continuous snowflakes
    fetch('data.json')
        .then(res => res.json())
        .then(data => {
            const total = data.medals.gold + data.medals.silver + data.medals.bronze;
            if (total > 0) {
                // Start continuous snowflakes after a brief celebration
                setTimeout(triggerSnowflakes, 500);
                setTimeout(startContinuousSnowflakes, 4000); // Start continuous after initial burst
            }
        })
        .catch(err => console.error('Error checking initial medals:', err));
});

// Refresh data every 5 minutes
setInterval(loadData, 5 * 60 * 1000);
