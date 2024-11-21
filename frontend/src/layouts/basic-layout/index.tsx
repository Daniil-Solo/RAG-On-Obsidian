import {Container, Group} from '@mantine/core';
import {NavLink} from "react-router-dom";
import "./index.css";

const LINKS = [
    {
        title: "Chat",
        url: "/chat"
    },
    {
        title: "Index",
        url: "/index"
    },
    {
        title: "Settings",
        url: "/settings"
    },
]

export interface BasicLayoutProps  {
    children: React.ReactNode
}


const BasicLayout = (props: BasicLayoutProps) => {
    return (
        <Container fluid={false} size="lg">
            <div style={{height: "100vh"}}>
                <Group h={"10%"} component={"nav"} justify="center">
                    {
                        LINKS.map(element => (
                            <NavLink key={element.title} className={"navbar__link"} to={element.url} end>
                                {element.title}
                            </NavLink>
                        ))
                    }
                </Group>
                <main style={{height: "90%"}}>
                    {props.children}
                </main>
            </div>
      </Container>
    );
}

export default BasicLayout;