import {Container, Group, Space} from '@mantine/core';
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
        <Container size="md">
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
                <Space h={"5%"}/>
                <main style={{height: "85%"}}>
                    {props.children}
                </main>
            </div>
      </Container>
    );
}

export default BasicLayout;