// URL di base del server Flask
const BASE_URL = 'http://localhost:5000';  // Modifica in base al tuo setup

async function apiRequest(endpoint, method, data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };
        if (data) {
            options.body = JSON.stringify(data);
        }
        const response = await fetch(`${BASE_URL}${endpoint}`, options);
        const result = await response.json();
        console.log(result);
    } catch (error) {
        console.error(`Errore durante la richiesta a ${endpoint}:`, error);
    }
}

/**
 * Registra un nuovo utente.
 * @param {Object} data - Oggetto con le seguenti proprietà:
 *   - username: Il nome utente.
 *   - password: La password dell'utente.
 *   - voter: Il nome dell'account votante.
 *   - interval: Intervallo di tempo per l'attività.
 *   - posting_key: La chiave di posting.
 */
async function registerUser(data) {
    await apiRequest('/register', 'POST', data);
}

/**
 * Effettua il login di un utente.
 * @param {Object} data - Oggetto con le seguenti proprietà:
 *   - username: Il nome utente.
 *   - password: La password dell'utente.
 */
async function loginUser(data) {
    await apiRequest('/login', 'POST', data);
}

/**
 * Configura un autore per un utente.
 * @param {Object} data - Oggetto con le seguenti proprietà:
 *   - username: Il nome utente associato all'autore.
 *   - author_name: Il nome dell'autore.
 *   - vote_percentage: Percentuale di voto.
 *   - post_delay_minutes: Ritardo in minuti prima di votare.
 *   - daily_vote_limit: Limite di voti giornalieri.
 *   - add_comment: Booleano per aggiungere un commento.
 *   - add_image: Booleano per aggiungere un'immagine.
 *   - comment_text: Testo del commento (opzionale).
 *   - image_path: Percorso dell'immagine (opzionale).
 */
async function configureAuthor(data) {
    await apiRequest('/configure_author', 'POST', data);
}

/**
 * Ottieni la lista degli autori configurati per un utente.
 * @param {String} username - Il nome utente.
 */
async function getAuthors(username) {
    await apiRequest(`/get_authors/${username}`, 'GET');
}

/**
 * Elimina un autore configurato per un utente.
 * @param {Object} data - Oggetto con le seguenti proprietà:
 *   - username: Il nome utente associato all'autore.
 *   - author_name: Il nome dell'autore da eliminare.
 */
async function deleteAuthor(data) {
    await apiRequest('/delete_author', 'POST', data);
}

/**
 * Aggiorna le informazioni di un autore configurato per un utente.
 * @param {Object} data - Oggetto con le seguenti proprietà:
 *   - username: Il nome utente associato all'autore.
 *   - author_name: Il nome dell'autore da aggiornare.
 *   - vote_percentage: Nuova percentuale di voto.
 *   - post_delay_minutes: Nuovo ritardo in minuti prima di votare.
 *   - daily_vote_limit: Nuovo limite di voti giornalieri.
 *   - add_comment: Booleano per aggiungere un commento.
 *   - add_image: Booleano per aggiungere un'immagine.
 *   - comment_text: Testo del commento (opzionale).
 *   - image_path: Percorso dell'immagine (opzionale).
 */
async function updateAuthor(data) {
    await apiRequest('/update_author', 'POST', data);
}

async function getAll() {
    await apiRequest('/get_all', 'GET');
}
export { registerUser, loginUser, configureAuthor, getAuthors, deleteAuthor, updateAuthor , getAll};
//usage examples
// registerUser({
//     username: 'test',
//     password: 'test',
//     voter: 'test',
//     interval: 10,
//     posting_key: '5JXN3YbJbYQ6z1e8wQ4jVtJ5mV6v5k5hZj1v1e8wQ4jVtJ5mV6v5k5hZj1v'
// });

// loginUser({
//     username: 'test',
//     password: 'test'
// });

// configureAuthor({
//     username: 'test',
//     author_name: 'author',
//     vote_percentage: 100,
//     post_delay_minutes: 60,
//     daily_vote_limit: 10,
//     add_comment: true,
//     add_image: true,
//     comment_text: 'Great post!',
//     image_path: 'image.jpg'
// });

// getAuthors('test');

// deleteAuthor({
//     username: 'test',
//     author_name: 'author'
// });

// updateAuthor({
//     username: 'test',
//     author_name: 'author',
//     vote_percentage: 50,
//     post_delay_minutes: 30,
//     daily_vote_limit: 5,
//     add_comment: false,
//     add_image: false
// });

