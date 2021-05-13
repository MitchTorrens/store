use std::io;
use termion::raw::IntoRawMode;
use tui::Terminal;
use tui::backend::TermionBackend;
use tui::widgets::{Widget, Block, Borders};
use tui::layout::{Layout, Constraint, Direction};
// use serde_derive::Deserialize

struct Actor {}

enum Entity {
    Actor(),
}

struct GameState {
    map: Map,
    entities: Vec<Option<Entity>>
}

fn inital_game_state(int32, int32) -> GameState {
    let mut gs = GameState { 
        map: 
    }
}

#[derive(Default)]
struct Config {
    map_width: i32,
    map_height: i32,
}

fn main() -> Result<(), io::Error> {
    let mut game_state = initial_game_state();


    // let stdout = io::stdout().into_raw_mode()?;
    // let backend = TermionBackend::new(stdout);
    // let mut terminal = Terminal::new(backend)?;
    // terminal.draw(|f| {
    //     let chunks = Layout::default()
    //         .direction(Direction::Vertical)
    //         .margin(1)
    //         .constraints(
    //             [
    //                 Constraint::Percentage(10),
    //                 Constraint::Percentage(80),
    //                 Constraint::Percentage(10)
    //             ].as_ref()
    //         )
    //         .split(f.size());
    //     let block = Block::default()
    //          .title("Block")
    //          .borders(Borders::ALL);
    //     f.render_widget(block, chunks[0]);
    //     let block = Block::default()
    //          .title("Block 2")
    //          .borders(Borders::ALL);
    //     f.render_widget(block, chunks[1]);
    // })?;
    Ok(())
}